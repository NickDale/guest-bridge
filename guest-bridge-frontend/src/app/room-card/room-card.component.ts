import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Room } from 'src/app/models/room';


@Component({
  selector: 'app-room-card',
  templateUrl: './room-card.component.html',
  styleUrls: ['./room-card.component.css']
})
export class RoomCardComponent {

  @Input() room!: Room; // A szoba adatai
  @Input() source!: 'szallas.hu' | 'vendegem'; // A forrás platform
  @Input() isMapped: boolean = false; // Csak a Szallas.hu oldalon kellhet
  @Input() mappedFrom: Room | undefined; // Csak a Vendégem oldalon kellhet

  // KIMENET (Esemény kibocsátása a szülő komponens felé)
  // Ezt használhatod a mappelési esemény indítására (pl. gombnyomásra)
  @Output() mapAction = new EventEmitter<Room>();

  // Segéd getter a könnyebb CSS/stíluskezeléshez
  get cardClass(): string {
    return this.source === 'szallas.hu' ? 'card-szallas' : 'card-vendegem';
  }

  // Akció végrehajtása (pl. mappelő gomb kattintása)
  performMapAction(): void {
    if (!this.isMapped) {
      // Kibocsátja az eseményt a szülő komponens felé, átadva a saját room objektumát
      this.mapAction.emit(this.room);
    }
  }
}
