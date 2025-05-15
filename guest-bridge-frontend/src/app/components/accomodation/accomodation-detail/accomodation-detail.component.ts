import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-accomodation-detail',
  templateUrl: './accomodation-detail.component.html',
  styleUrls: ['./accomodation-detail.component.css']
})
export class AccomodationDetailComponent {
  @Input() accommodationId: number | undefined;
}
