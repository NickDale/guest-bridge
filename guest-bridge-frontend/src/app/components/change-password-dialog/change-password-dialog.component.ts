import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-change-password-dialog',
  templateUrl: './change-password-dialog.component.html',
  styleUrls: ['./change-password-dialog.component.css']
})
export class ChangePasswordDialogComponent {
  oldPassword = '';
  newPassword = '';
  confirmPassword = '';


  passwordChangeForm = this.formBuilder.group({
    oldPassword: ['', [Validators.required,Validators.minLength(6), Validators.max(16)]],
    newPassword: ['', [Validators.required, Validators.minLength(6), Validators.max(16)]], //TODO: pattern?
    confirmPassword: ['', [Validators.required, Validators.minLength(6), Validators.max(16)]]
  });

  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<ChangePasswordDialogComponent>
  ) { }

  changePassword() {
    if (this.newPassword !== this.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    // call service to update password...

    this.dialogRef.close();
  }
}
