import { Component, Input, SimpleChanges } from '@angular/core';
import { ConnectionType, Property } from 'src/app/models/property-connection';
import { AccommodationService } from 'src/app/services/accommodation.service';

@Component({
  selector: 'app-connection-comp',
  templateUrl: './connections.component.html',
  styleUrls: ['./connections.component.css']
})
export class ConnectionsComponent {
  @Input() accommodationId?: number;
  @Input() type?: ConnectionType;
  loading = false;
  isEditing = false;

  property?: Property;
  constructor(
    private accomodationService: AccommodationService
  ) { }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['accommodationId'] && this.accommodationId !== undefined) {
      this.loadConnectionDetail();
    }
  }

  loadConnectionDetail(): void {
    this.loading = true;

    setTimeout(() => {
      this.accomodationService.findByIdAndType(this.accommodationId!, this.type!).subscribe(
        p => this.property = p
      );
      this.loading = false;
    }, 500);
  }

  toggleEdit() {
    this.isEditing = !this.isEditing;
    /*if (this.isEditing) {
      this.accomodationForm.enable();
    } else {
      this.accomodationForm.disable();
    }*/
  }

  save() {

  }

  openModal(property:Property) {

  }
}
