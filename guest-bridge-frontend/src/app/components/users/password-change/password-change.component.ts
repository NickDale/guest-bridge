import { Component, ElementRef, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';
import { AccommodationService } from 'src/app/services/accommodation.service';

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
    private elementRef: ElementRef
  ) { }

  ngOnInit(): void {
    this.passwordChangeForm = this.fb.group({
      origPassword: ['', Validators.required, Validators.minLength(4)]
    });
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

  }

  closeModal() {
    const modalEl = this.elementRef.nativeElement.closest('.modal');
    // const modalInstance = bootstrap.Modal.getInstance(modalEl);
    // modalInstance.hide();
  }

  resetForm(): void {
    this.errorMessage = null;
    this.submitted = false;
    this.passwordChangeForm.reset();
  }
}
