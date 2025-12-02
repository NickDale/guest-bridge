import { Component } from '@angular/core';
import { User } from 'src/app/models/user';
import { UserService } from 'src/app/services/user.service';
import { FormBuilder, Validators } from '@angular/forms';

declare var bootstrap: any;
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

  //openChangePasswordDialog(): void {
    //this.dialog.open(ChangePasswordDialogComponent);
  //}


  toggleEdit() {
    this.isEditing = !this.isEditing;
    if (this.isEditing) {
      this.userForm.enable();
    } else {
      this.disable();
    }
  }

  private disable() {
    this.userForm.disable();
    this.pattchForm();
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
    if (!this.userForm.valid) {
      alert('Form is invalid');
    }

    const {
      full_name, email, billingName, billingEmail,
      tax, postcode, city, street, streetNr, floor, door
    } = this.userForm.value;

    this.userService.updateUser(this.user.id, {
      full_name: full_name!,
      email: email!,
      billing_info: {
        id: this.user.billing_info.id,
        name: billingName!,
        email: billingEmail,
        country: 'Magyarország',
        postcode: postcode,
        tax: tax,
        city: city,
        street: street,
        street_number: streetNr,
        floor: floor,
        door: door
      }

    }).subscribe({
      next: success => {
        if (success) {
          this.userService.getUserById(this.user.id).subscribe(user => {
            this.user = user
            this.userService.setSelectedUser(this.user);
          })
          this.toggleEdit()
        }

      },
      error: error => {
        console.error('Hiba a regisztráció során:', error);
      }
    });
  }

  closeModal(modalId: string): void {
    const modalElement = document.getElementById(modalId);
    if (modalElement) {
      const modalInstance = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
      modalInstance.hide();
    }
  }

  close() {
    alert("Sikeres jelszóváltoztatás!");
  }
}
