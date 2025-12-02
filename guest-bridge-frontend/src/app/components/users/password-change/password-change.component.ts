import { Component, ElementRef, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ValidatorFn, AbstractControl } from '@angular/forms';
import { throwError } from 'rxjs/internal/observable/throwError';
import { catchError } from 'rxjs/internal/operators/catchError';
import { UserService } from 'src/app/services/user.service';

declare var bootstrap: any;
@Component({
  selector: 'app-password-change',
  templateUrl: './password-change.component.html',
  styleUrls: ['./password-change.component.css']
})
export class PasswordChangeComponent {

  @Output() passwordChanged = new EventEmitter<void>();
  @Input() selectedUserId!: number;

  passwordChangeForm!: FormGroup;
  submitted = false;
  errorMessage: string | null = null;
  origPasswordFieldType: 'password' | 'text' = 'password';
  newPasswordFieldType: 'password' | 'text' = 'password';
  confimPasswordFieldType: 'password' | 'text' = 'password';

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private elementRef: ElementRef
  ) { }

  ngOnInit(): void {
    this.passwordChangeForm = this.fb.group(
      {
        origPassword: ['', [Validators.required]],
        newPassword: ['', [Validators.required, Validators.minLength(4)]],
        confirmPassword: ['', [Validators.required, Validators.minLength(4)]]
      },
      {
        validator: this.passwordMatchValidator('newPassword', 'confirmPassword')
      }
    );
  }

  passwordMatchValidator(passwordControlName: string, confirmControlName: string): ValidatorFn {
    return (formGroup: AbstractControl): { [key: string]: any } | null => {
      const passwordControl = formGroup.get(passwordControlName);
      const confirmControl = formGroup.get(confirmControlName);

      if (!passwordControl || !confirmControl || confirmControl.errors && confirmControl.errors['mustMatch']) {
        return null;
      }

      if (passwordControl.value !== confirmControl.value) {
        confirmControl.setErrors({ mustMatch: true });
        return { mustMatch: true };
      } else {
        if (confirmControl.errors && confirmControl.errors['mustMatch']) {
          confirmControl.setErrors(null);
        }
        return null;
      }
    };
  }

  togglePasswordVisibility(field: 'orig' | 'new' | 'confirm'): void {
    switch (field) {
      case 'orig':
        this.origPasswordFieldType = this.origPasswordFieldType === 'password' ? 'text' : 'password';
        break;
      case 'new':
        this.newPasswordFieldType = this.newPasswordFieldType === 'password' ? 'text' : 'password';
        break;
      case 'confirm':
        this.confimPasswordFieldType = this.confimPasswordFieldType === 'password' ? 'text' : 'password';
        break;
    }
  }

  get form() { return this.passwordChangeForm.controls; }

  onSubmit(): void {
    this.submitted = false;
    this.errorMessage = null;
    if (this.passwordChangeForm.invalid) {
      this.passwordChangeForm.markAllAsTouched();
      return;
    }

    const { origPassword, newPassword } = this.passwordChangeForm.value;

    this.userService.changePassword(this.selectedUserId, origPassword, newPassword)
      .pipe(
        catchError(error => {
          this.errorMessage = 'Hiba a jelszó módosítása során. Ellenőrizze az eredeti jelszót.';
          return throwError(() => error);
        })
      )
      .subscribe({
        next: success => {
        //  alert('Jelszó sikeresen módosítva!');
          this.passwordChanged.emit();
          this.closeModal();
        },
        error: () => {
          alert('Hiba a jelszó módosítása közben');
        }
      });
  }

  closeModal() {
    const modalEl = this.elementRef.nativeElement.closest('.modal');
    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    modalInstance.hide();
  }

  resetForm(): void {
    this.submitted = true;
    this.errorMessage = null;
    this.passwordChangeForm.reset();
  }
}
