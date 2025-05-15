import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { User } from 'src/app/models/user';
import { UserService } from 'src/app/services/user.service';
import { ChangePasswordDialogComponent } from '../../change-password-dialog/change-password-dialog.component';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';

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
    username: [{ value: '', disabled: !this.isEditing }, Validators.required],
    billingAddress: [{ value: '', disabled: !this.isEditing }, Validators.required]
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
      username: this.user.username
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
