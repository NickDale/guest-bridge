import threading
import time
import uuid
from datetime import datetime

from fastapi import HTTPException
from playwright.sync_api import sync_playwright, Error
from sqlalchemy.orm import Session
from starlette import status

from app.models.models import Accommodation
from app.routers.schemas import ExternalLoginRequest, ExternalAuth2FAVerifyRequest
from app.services import accommodation_service
from app.services.auth_service import USER_ID
from app.services.syncronisation_service import start_sync
from app.services.szallas_hu.constatnt import BASE_SZALLAS_HU_URL
from app.services.vendegem.vendegem_connection import connect_to_vendegem

playwright_sessions = {}


def list_all_accommodation_from_vendegem():
    vendegem = connect_to_vendegem()
    return vendegem.visible_accommodations()


def list_rooms_for_accommodation(accommodation_id: int, db: Session):
    # TODO: validate user visibility for accomodation

    accommodation = (
        db.query(
            Accommodation.vendegem_external_id.label("vendegem_id"),
            Accommodation.vendegem_external_ref.label("vendegem_ref")
        )
        # .join(UserAccommodation, UserAccommodation.accommodation_id == Accommodation.id)
        # .join(User, User.id == UserAccommodation.user_id)
        .filter(
            # UserAccommodation.user_id == user_id,
            Accommodation.id == accommodation_id
        )
        .first()
    )
    print(accommodation.vendegem_id)
    vendegem = connect_to_vendegem()
    return vendegem.rooms_by_id(accommodation.vendegem_id)


def check_accommodation_connection(accommodation_id: int, connection_type: str, db: Session):
    if 'SZALLAS_HU' == connection_type:
        return False

    if 'VENDEGEM' == connection_type:
        accommodation = accommodation_service.find_accommodation_by_id(db, accommodation_id)
        if accommodation is None:
            return False
        else:
            vendegem = connect_to_vendegem()
            visible_accommodations_in_vendegem = vendegem.visible_accommodations
            try:
                found_accommodation = next(
                    (ac for ac in visible_accommodations_in_vendegem if
                     ac.name == accommodation['name'] and ac.id == accommodation['vendegem_external_id']),
                    None
                )
                if found_accommodation:
                    return True
            except Exception as e:
                print(f"Hiba történt a keresés során: {e}")
                return False

    return False


def external_login(accommodation_id: int,
                   connection_type: str,
                   ext_login_request: ExternalLoginRequest,
                   logged_user,
                   db: Session):
    if connection_type == 'SZALLAS_HU':
        session_id = szallas_hu_connection(ext_login_request, accommodation_id, logged_user, db)
        return {
            "session_id": session_id
        }
    else:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


def session_status_check(accommodation_id: int,
                         connection_type: str,
                         session_id: str):
    if connection_type == 'SZALLAS_HU':

        pw_session = playwright_sessions[session_id]
        return {
            "step": pw_session['step'],
            "session_id": session_id,
            "last_update": pw_session['last_update']
        }
    else:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


def external_login_verification(accommodation_id: int,
                                connection_type: str,
                                verify_request: ExternalAuth2FAVerifyRequest,
                                verified_user):
    if connection_type == 'SZALLAS_HU':
        pw_session = playwright_sessions[verify_request.session_id]
        pw_session["2fa_code"] = verify_request.code
        pw_session["last_update"] = time.time()
        pw_session["step"] = "2fa_verify"

    else:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


def szallas_hu_connection(ext_login_request: ExternalLoginRequest,
                          accommodation_id: int,
                          logged_user,
                          db: Session) -> str:
    session_id = str(uuid.uuid4())
    accommodation = accommodation_service.accommodation_by_id(accommodation_id, db)
    if not accommodation.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accommodation is inactive")

    playwright_sessions[session_id] = {
        "step": "started",
        "browser": None,
        "page": None,
        "2fa_code": None,
        "data": {
            'accommodation_id': accommodation_id,
            'started_by': logged_user[USER_ID],
        },
        "last_update": time.time(),
    }
    threading.Thread(
        target=szallas_hu_login_flow,
        args=(session_id, ext_login_request.username, ext_login_request.password)
    ).start()

    return session_id


def szallas_hu_login_flow(session_id: str, username: str, password: str):
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False)

        # local test
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.new_page()

        p_session = playwright_sessions[session_id]
        p_session["browser"] = browser
        p_session["page"] = page
        p_session["step"] = "login"
        p_session["last_update"] = time.time()

        page.goto(url=BASE_SZALLAS_HU_URL)

        cookies_confirm_btn_selector = 'button:has-text("Elfogadom")'
        has_to_confirm = page.locator(cookies_confirm_btn_selector).count() > 0
        if has_to_confirm:
            page.click(cookies_confirm_btn_selector, timeout=5000)
        else:
            print("no cookies conformation required")

        email_selector = 'input[name="email"]'
        password_selector = 'input[name="password"]'
        mfa_token_selector = 'input[name="mfaToken"]'

        page.fill(email_selector, username)
        page.fill(password_selector, password)
        page.click('button[type="submit"]')

        time.sleep(0.5)
        has_mfa = page.locator(mfa_token_selector).count() > 0

        if has_mfa:
            p_session["step"] = "waiting_2fa"
            p_session["last_update"] = time.time()

        while p_session["step"] == "waiting_2fa":
            time.sleep(0.5)
            print("waiting.......")
            p_session["last_update"] = time.time()

        if p_session["step"] == "2fa_verify":
            code = p_session["2fa_code"]
            page.fill(mfa_token_selector, code)
            page.click('button[type="submit"]')
            print(f' kód beszúrva  = {code}')
        else:
            print(f' kód beszúrás kihagyása ....')

        time.sleep(1)

        modal_selector = '.modal-dialog'
        close_button_selector = 'a.btn.btn-default[data-notify-url*="skip=noployaltyextradiscountspopup"]'

        modal = page.locator(modal_selector)

        if modal.count() > 0 and modal.first.is_visible():
            print("Modal megjelent.")

            if page.locator(close_button_selector).count() > 0:
                page.locator(close_button_selector).click()

                page.wait_for_selector(modal_selector, state="detached")
                print("Modal bezárva.")

        try:
            p_session["step"] = "sync_started"
            start_sync(page,
                       p_session["data"]['accommodation_id'],
                       str(p_session["data"]['started_by']),
                       from_date=datetime(2025, 9, 1),
                       to_date=datetime(2025, 11, 1)
                       )
            p_session["step"] = "done"
            p_session["last_update"] = time.time()
        except Error:
            p_session["step"] = "sync_failed"

        while p_session["step"] not in ['sync_failed', 'done']:
            print("waiting.....")
            time.sleep(1)
