import { Component, ElementRef, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { catchError, throwError } from 'rxjs';
import { ConnectionType } from 'src/app/models/property-connection';
import { AccommodationService } from 'src/app/services/accommodation.service';


declare var bootstrap: any;
@Component({
  selector: 'app-sync-start',
  templateUrl: './sync-start.component.html',
  styleUrls: ['./sync-start.component.css']
})
export class SyncStartComponent {


  @Output() syncStarted = new EventEmitter<void>();
  @Input() selectedAccommodationId!: number;

  szallasHuLoginForm!: FormGroup;
  submitted = false;
  errorMessage: string | null = null;
  passwordFieldType: 'password' | 'text' = 'password';


  sessionId: string | null = null;
  is2FaRequired = false;
  isProcessing = false;
  twoFactorForm!: FormGroup;


  constructor(
    private fb: FormBuilder,
    private accommodationService: AccommodationService,
    private elementRef: ElementRef
  ) { }

  ngOnInit(): void {
    this.szallasHuLoginForm = this.fb.group(
      {
        password: ['', [Validators.required]],
        username: ['', [Validators.required, Validators.email]]
      }
    );

    this.twoFactorForm = this.fb.group({
      twoFactorCode: ['', [Validators.required, Validators.pattern('^[0-9]{6}$')]]
    });
  }

  togglePasswordVisibility(): void {
    this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
  }

  get form() { return this.szallasHuLoginForm.controls; }

  onSubmit(): void {
    this.submitted = false;
    this.errorMessage = null;
    if (this.szallasHuLoginForm.invalid) {
      this.szallasHuLoginForm.markAllAsTouched();
      return;
    }
    this.isProcessing = true;
    const { username, password } = this.szallasHuLoginForm.value;

    this.accommodationService.externalLogin(this.selectedAccommodationId, ConnectionType.SZALLAS_HU, username, password)
      .pipe(
        catchError(error => {
          this.errorMessage = 'Hiba a bejelentkezés során. Ellenőrizze az adatokat.';
          return throwError(() => error);
        })
      )
      .subscribe({
        next: status => {
          this.isProcessing = false;

          console.log("nnnnnnnn")
          console.log("status.step")
          console.log(status.step)
          if (status.step === 'waiting_2fa') {
            this.sessionId = status.session_id;
            this.is2FaRequired = true;
            this.szallasHuLoginForm.disable();

          } else if (status.step === 'failed') {
              console.log("failed")
            this.errorMessage = 'Ismeretlen hiba a bejelentkezési folyamat során.';
          } else {
            console.log("ELSE")
            this.syncStarted.emit();
            this.closeModal();
          }
        },
        error: error => {
          this.isProcessing = false;
          this.errorMessage = error.message || 'Hiba történt a bejelentkezés kezdeményezésekor.';
        }
      });
  }

  submit2faCode(): void {
    this.submitted = true;
    this.errorMessage = null;

    if (this.twoFactorForm.invalid || !this.sessionId) {
      this.twoFactorForm.markAllAsTouched();
      return;
    }

    const code = this.twoFactorForm.value.twoFactorCode;

    this.isProcessing = true;
    this.accommodationService.submit2faCode(this.selectedAccommodationId, ConnectionType.SZALLAS_HU, this.sessionId, code)
      .subscribe({
        next: () => {
          this.is2FaRequired = false;
          this.isProcessing = false;
          this.syncStarted.emit();
          this.closeModal();
        },
        error: error => {
          this.isProcessing = false;
          this.errorMessage = error.error_message || 'Hibás 2FA kód vagy hiba a beküldés során.';
          this.twoFactorForm.get('twoFactorCode')?.reset();
        }
      });
  }

  closeModal() {
    const element = this.elementRef.nativeElement.closest('.modal');
    const modalInstance = bootstrap.Modal.getInstance(element);
    modalInstance.hide();
  }

  resetForm(): void {
    this.submitted = true;
    this.errorMessage = null;
    this.szallasHuLoginForm.reset();
  }
}
