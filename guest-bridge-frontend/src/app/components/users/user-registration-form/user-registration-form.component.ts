import { Component, ElementRef, EventEmitter, OnInit, Output } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ValidatorFn, AbstractControl } from '@angular/forms';
import { UserService } from 'src/app/services/user.service';

declare var bootstrap: any;
@Component({
  selector: 'app-user-registration-form',
  templateUrl: './user-registration-form.component.html',
  styleUrls: ['./user-registration-form.component.css']
})
export class UserRegistrationFormComponent implements OnInit {

  @Output() userAdded = new EventEmitter<void>();

  userForm!: FormGroup;
  submitted = false;
  errorMessage: string | null = null;

  constructor(private fb: FormBuilder, private userService: UserService, private elementRef: ElementRef) { }

  ngOnInit(): void {
    this.userForm = this.fb.group({
      fullName: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]]
    });
  }

  get form() { return this.userForm.controls; }

  onSubmit(): void {
    this.submitted = true;
    if (this.userForm.invalid) {
      return;
    }

    const { fullName, email } = this.userForm.value;
    this.userService.registerUser(fullName, email).subscribe({
      next: success => {
        if (success) {
          this.resetForm();
          this.userAdded.emit();
        }
        this.closeModal();
      },
      error: error => {
        console.error('Hiba a regisztráció során:', error);
        this.errorMessage = `Hiba: ${error.error.detail}`;
      }
    });
  }

  closeModal() {
    const modalEl = this.elementRef.nativeElement.closest('.modal');
    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    modalInstance.hide();
  }

  resetForm(): void {
    this.errorMessage = null;
    this.submitted = false;
    this.userForm.reset();
  }
}