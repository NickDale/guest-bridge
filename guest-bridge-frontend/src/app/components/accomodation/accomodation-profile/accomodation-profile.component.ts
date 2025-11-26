import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { AccomodationDetail } from 'src/app/models/accommodation';
import { ConnectionType } from 'src/app/models/property-connection';
import { AccommodationService } from 'src/app/services/accommodation.service';

@Component({
  selector: 'app-accomodation-profile',
  templateUrl: './accomodation-profile.component.html',
  styleUrls: ['./accomodation-profile.component.css']
})
export class AccomodationProfileComponent {

  accommodationId: number | undefined;
  loading = false;
  isEditing = false;
  accommodation!: AccomodationDetail;

  accomodationForm = this.fb.group({
    contactName: [{ value: this.accommodation?.contact_name, disabled: !this.isEditing }],
    contactPhone: [{ value: this.accommodation?.contact_phone, disabled: !this.isEditing }],
    contactEmail: [{ value: this.accommodation?.contact_email, disabled: !this.isEditing }]
  });

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private accommodationService: AccommodationService
  ) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.accommodationId = +id;
        this.fetchAccommodation();
      }
    });
    this.isEditing = false;
  }

  toggleEdit(): void {
    this.isEditing = !this.isEditing;
    this.isEditing ? this.accomodationForm.enable() : this.accomodationForm.disable();
  }

  save(): void {
    if (this.accomodationForm.valid) {
      alert('Form submitted - ' + this.accomodationForm.value);
      // itt jöhetne egy save/update service hívás
    } else {
      alert('Form is invalid');
    }
    this.toggleEdit();
  }

  get szallas_hu() {
    return ConnectionType.SZALLAS_HU;
  }

  get vendegem() {
    return ConnectionType.VENDEGEM;
  }

  private fetchAccommodation(): void {
    this.loading = true;

    setTimeout(() => {
      this.accommodationService.getById(this.accommodationId!).subscribe({
        next: (accommodation) => {
          if (accommodation) {
            this.accommodation = accommodation;
            this.accommodationService.setSelected(accommodation);
            this.updateForm(accommodation);
            this.loading = false;
          } else {
          }
        },
        error: (err) => {
          console.error('Failed to fetch accommodation', err);
          this.loading = false;
        }
      });
      this.loading = false;
    }, 600);

  }

  private updateForm(accommodation: AccomodationDetail): void {
    this.accomodationForm.setValue({
      contactName: accommodation.contact_name,
      contactEmail: accommodation.contact_email,
      contactPhone: accommodation.contact_phone
    });
    this.isEditing ? this.accomodationForm.enable() : this.accomodationForm.disable();
  }

  get addressString(): String {
    const address = this.accommodation.address;
    return [
      address.postcode,
      address.city,
      address.street,
      address.street_number
    ].filter(part => !!part).join(', ');
  }

  get isAccommodationActive(): boolean {
    return this.accommodation.status.toUpperCase() === 'ACTIVE';
  }

  get statusText(): string {
    return this.isAccommodationActive ? 'Aktív' : 'Inaktív';
  }

  get statusClass(): string {
    return this.isAccommodationActive ? 'text-success' : 'text-danger';
  }

}
