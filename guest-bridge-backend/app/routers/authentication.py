import asyncio
import threading
import time
import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from playwright.async_api import async_playwright
from sqlalchemy.orm import Session
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Page

from app.core.database import get_db
from app.routers import schemas
from app.services import auth_service
from app.services.szallas_hu.constatnt import base_szallas_hu_url

router = APIRouter(prefix="/authentications", tags=["Authentication"])


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_resp = auth_service.login(username=form_data.username, password=form_data.password, db=db)
    return {"access_token": auth_resp['access_token'], "token_type": auth_resp['token_type']}


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    return auth_service.login(username=request.username, password=request.password, db=db)

    # acc = [a for a in v.visible_accommodations if a.name == 'Jázmin Apartmanház'][0]

    # v.reservations(acc.id)

    # pppp()
    # todo: ez működik
    # session_id = str(uuid.uuid4())
    # playwright_sessions[session_id] = {
    #     "step": "started",
    #     "browser": None,
    #     "page": None,
    #     "2fa_code": None,
    #     "last_update": time.time(),
    # }
    # threading.Thread(
    #     target=run_playwright_flow,
    #     args=(session_id, "username", "password")
    # ).start()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # return LoginResponse(
    #     id=user.id,
    #     username=user.username,
    #     full_name=user.full_name,
    #     email=user.email,
    #     role=user.user_type.name,
    # )


PLAYWRIGHT_PAGE_CACHE: dict[str, Page] = {}


def pppp():
    with (sync_playwright() as pw):
        # async with (async_playwright() as pw):
        browser = pw.chromium.launch(
            headless=False,
            slow_mo=600
        )
        context = browser.new_context()
        page = browser.new_page()
        page.goto(url=base_szallas_hu_url)

        login_form_selector = '#login-form'

        # 1. Email mező kitöltése a formon belül
        email_selector = 'input[name="email"]'
        password_selector = 'input[name="password"]'

        # page.wait_for_load_state("networkidle")
        page_content = page.content()
        # if ('Mielőtt továbblép' in page_content and 'összes elfogad' in page_content) \
        #         or ('continue to Google' in page_content and 'Accept all' in page_content):
        #     page.locator(
        #         f'//span[@class="{REJECT_ALL_SPAM_ID}"]'
        #     ).first.click()  # cookie-k elutasítása
        page.click('button:has-text("Elfogadom")', timeout=5000)

        page.fill(email_selector, 'dsfsfsd@sfdfsdf.com')
        page.fill(password_selector, 'dsfsfsd')

        page.click('button[type="submit"]')

        SESSION_ID = str(uuid.uuid4())
        PLAYWRIGHT_PAGE_CACHE[SESSION_ID] = page
        print(SESSION_ID)
        # await page.fill(email_selector, user_email)

        # 2. Jelszó mező kitöltése a formon belül
        # await page.fill(password_selector, user_password)

    browser.close()


playwright_sessions = {}


def run_playwright_flow(session_id: str, username: str, password: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Save into global store
        s = playwright_sessions[session_id]
        s["browser"] = browser
        s["page"] = page
        s["step"] = "waiting_2fa"
        s["last_update"] = time.time()

        # LOGIN PAGE FLOW (legacy page)
        page.goto(url=base_szallas_hu_url)

        page.click('button:has-text("Elfogadom")', timeout=5000)

        email_selector = 'input[name="email"]'
        password_selector = 'input[name="password"]'

        page.fill(email_selector, 'dsfsfsd@sfdfsdf.com')
        page.fill(password_selector, 'dsfsfsd')
        page.click('button[type="submit"]')

        # Wait until 2FA is entered
        while s["step"] == "waiting_2fa":
            time.sleep(0.5)
            s["last_update"] = time.time()

        code = s["2fa_code"]
        page.fill("#2fa_code", code)
        page.click("#confirm")

        s["step"] = "done"
        s["last_update"] = time.time()
