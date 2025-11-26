import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Room } from 'src/app/models/room';


@Component({
  selector: 'app-room-card',
  templateUrl: './room-card.component.html',
  styleUrls: ['./room-card.component.css']
})
export class RoomCardComponent {

  @Input() room!: Room;
  @Input() source!: 'szallas.hu' | 'vendegem';
  @Input() isMapped: boolean = false;
  @Input() mappedFrom: Room | undefined;

  @Output() mapAction = new EventEmitter<Room>();

  get cardClass(): string {
    return this.source === 'szallas.hu' ? 'card-szallas' : 'card-vendegem';
  }

  performMapAction(): void {
    if (!this.isMapped) {
      this.mapAction.emit(this.room);
    }
  }
}
