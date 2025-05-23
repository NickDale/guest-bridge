import { Component } from '@angular/core';
import { Validators, FormBuilder } from '@angular/forms';
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
    address: [{ value: this.accommodation?.address, disabled: !this.isEditing }, [Validators.required]],
    contactName: [{ value: this.accommodation?.contact_name, disabled: !this.isEditing }],
    contactPhone: [{ value: this.accommodation?.contact_phone, disabled: !this.isEditing }],
    contactEmail: [{ value: this.accommodation?.contact_email, disabled: !this.isEditing }]
    //todo: add more
    //  address2: new FormControl({ value: this.accommodation?.address, disabled: !this.isEditing }, [Validators.required])

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
      console.log('Form submitted', this.accomodationForm.value);
      // itt jöhetne egy save/update service hívás
    } else {
      console.warn('Form is invalid');
    }
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
      address: accommodation.address,
      contactName :accommodation.contact_name,
      contactEmail:accommodation.contact_email,
      contactPhone:accommodation.contact_phone
    });
    this.isEditing ? this.accomodationForm.enable() : this.accomodationForm.disable();
  }

}
