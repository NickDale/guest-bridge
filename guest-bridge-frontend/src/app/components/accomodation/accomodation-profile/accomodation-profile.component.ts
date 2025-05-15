import { Component } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Accomodation } from 'src/app/models/accommodation';
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
  accommodation?: Accomodation;

  accomodationForm = new FormGroup({
    name: new FormControl({ value: this.accommodation?.name, disabled: !this.isEditing }, Validators.required),
    address: new FormControl({ value: this.accommodation?.address, disabled: !this.isEditing }, [Validators.required])
    //todo: add more
    //  address2: new FormControl({ value: this.accommodation?.address, disabled: !this.isEditing }, [Validators.required])

  });

  constructor(
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

  private updateForm(accommodation: Accomodation): void {
    this.accomodationForm.setValue({
      name: accommodation.name || '',
      address: accommodation.address || ''
    });
    this.isEditing ? this.accomodationForm.enable() : this.accomodationForm.disable();
  }




}
