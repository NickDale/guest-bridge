import { Component, ElementRef, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormGroup, FormBuilder, Validators, } from '@angular/forms';
import { AccommodationService } from 'src/app/services/accommodation.service';

declare var bootstrap: any;
@Component({
  selector: 'app-accomodation-registration-form',
  templateUrl: './accomodation-registration-form.component.html',
  styleUrls: ['./accomodation-registration-form.component.css']
})
export class AccomodationRegistrationFormComponent implements OnInit {

  @Output() accommodationAdded = new EventEmitter<void>();
  @Input() selectedUserId!: number;

  accommodationForm!: FormGroup;
  submitted = false;
  errorMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private accommodationService: AccommodationService,
    private elementRef: ElementRef
  ) { }

  ngOnInit(): void {
    this.accommodationForm = this.fb.group({
      name: ['', Validators.required],
      ntak: ['', Validators.required],
      postcode: [''],
      city: ['', Validators.required],
      street: ['', Validators.required],
      streetNo: ['', Validators.required],
      szallasHuId: ['', Validators.required],
      vendegemId: [''],
      vendegemRef: [''],
    });
  }

  get form() { return this.accommodationForm.controls; }

  onSubmit(): void {
    this.submitted = true;
    if (this.accommodationForm.invalid) {
      return;
    }
    if (!this.selectedUserId) {
      this.errorMessage = "Hiba: A felhasználó ID hiányzik.";
      return;
    }

    const { name, vendegemId, vendegemRef, ntak, szallasHuId,postcode,city,street,streetNo } = this.accommodationForm.value;
    this.accommodationService.registerNewAccommodation({
      name: name,
      user_id: this.selectedUserId,
      vendegem_id: vendegemId,
      szallas_hu_id: szallasHuId,
      ntak_no: ntak,
      vendegem_ref: vendegemRef,
      address: {
        postcode: postcode,
        country: 'Magyarország',
        city: city,
        street: street,
        street_number: streetNo,
        floor: null,
        door: null
      }

    }).subscribe({
      next: success => {
        if (success) {
          this.resetForm();
          this.accommodationAdded.emit();
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
    this.accommodationForm.reset();
  }
}