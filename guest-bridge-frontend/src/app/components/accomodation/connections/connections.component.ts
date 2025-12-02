import { Component, Input, SimpleChanges } from '@angular/core';
import { ConnectionStatus, ConnectionType, Property } from 'src/app/models/property-connection';
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

  openModal(property: Property) {
  }

  get szallasHuProperty(): boolean {
    if (!this.property) {
      return false;
    }
    return this.property.type === ConnectionType.SZALLAS_HU;
  }


  get showVendegemFailedCheckMessage(): boolean {
    if (!this.property) {
      return false;
    }

    return (
      this.property.type === ConnectionType.VENDEGEM &&
      this.property.status === ConnectionStatus.FAILED
    );
  }
}
