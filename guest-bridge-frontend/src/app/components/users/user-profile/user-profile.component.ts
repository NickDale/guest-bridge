import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { User } from 'src/app/models/user';
import { UserService } from 'src/app/services/user.service';
import { ChangePasswordDialogComponent } from '../../change-password-dialog/change-password-dialog.component';
import { FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent {
  user!: User;
  isEditing = false;
  loading = false;

  constructor(
    private fb: FormBuilder,
    private dialog: MatDialog,
    private userService: UserService) { }

  userForm = this.fb.group({
    full_name: [{ value: '', disabled: !this.isEditing }, Validators.required],
    email: [{ value: '', disabled: !this.isEditing }, [Validators.required, Validators.email]],
    billingName: [{ value: '', disabled: !this.isEditing }, Validators.required],
    billingEmail: [{ value: '', disabled: !this.isEditing }],
    tax: [{ value: '', disabled: !this.isEditing }],
    country: [{ value: '', disabled: !this.isEditing }],
    postcode: [{ value: '', disabled: !this.isEditing }],
    city: [{ value: '', disabled: !this.isEditing }],
    street: [{ value: '', disabled: !this.isEditing }],
    streetNr: [{ value: '', disabled: !this.isEditing }],
    floor: [{ value: '', disabled: !this.isEditing }],
    door: [{ value: '', disabled: !this.isEditing }],
  });

  ngOnInit() {
    this.userService.selectedUser$.subscribe(user => {
      if (user) {
        this.user = user;
        this.isEditing = false;
        this.pattchForm();
      }
    });
  }

  openChangePasswordDialog(): void {
    this.dialog.open(ChangePasswordDialogComponent);
  }

  toggleEdit() {
    this.isEditing = !this.isEditing;
    if (this.isEditing) {
      this.userForm.enable();
    } else {
      this.userForm.disable();
      this.pattchForm();
    }
  }

  private pattchForm() {
    this.userForm.patchValue({
      full_name: this.user.full_name,
      email: this.user.email,
      billingName: this.user.billing_info.name,
      billingEmail: this.user.billing_info.email,
      tax: this.user.billing_info.tax,
      country: this.user.billing_info.country,
      postcode: this.user.billing_info.postcode,
      city: this.user.billing_info.city,
      street: this.user.billing_info.street,
      streetNr: this.user.billing_info.street_number,
      floor: this.user.billing_info.floor,
      door: this.user.billing_info.door,
    });
  }

  onSubmit() {
    if (this.userForm.valid) {
      console.log('Form submitted', this.userForm.value);
    } else {
      console.log('Form is invalid');
    }
  }
}
