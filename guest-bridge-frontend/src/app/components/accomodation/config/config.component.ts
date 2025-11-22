import { Component, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MappedViewItem, Room, RoomMapping } from 'src/app/models/room';
import { ConfigService } from 'src/app/services/config.service';

@Component({
  selector: 'app-accommodation-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.css']
})
export class ConfigComponent {
  @Input() accommodationId?: number;

  szallasHuRooms: Room[] = [];
  vendegemRooms: Room[] = [];
  currentMapping: RoomMapping = {};
  mappedViewData: MappedViewItem[] = [];

  loading: boolean = true;

  constructor(
    private configService: ConfigService,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.accommodationId = +id;
        this.fetchAccommodation();
      }
    });
  }

  fetchAccommodation(): void {
    this.loading = true;

    this.configService.listAccommoddationMappingConfiguration(this.accommodationId!).subscribe({
      next: (data) => {
        this.szallasHuRooms = data.szallasHuRooms;
        this.vendegemRooms = data.vendegemRooms;
        this.currentMapping = data.mapping;

        this.prepareMappedViewData();
        this.loading = false;
      },
      error: (err) => {
        console.error('Hiba az adatok lekérésekor:', err);
        this.loading = false;
      }
    });
  }

  prepareMappedViewData(): void {
    const allMappedItems: MappedViewItem[] = this.szallasHuRooms.map(szhRoom => {
      let vendegemRoom: Room | null = null;
      const id = this.currentMapping[szhRoom.id];
      if (id) {
        vendegemRoom = this.vendegemRooms.find(r => r.id == +id) || null;
      }
      return {
        szallasHuRoom: szhRoom,
        vendegemRoom: vendegemRoom
      };
    });

    const mappedAndSorted: MappedViewItem[] = allMappedItems
      .filter(item => item.vendegemRoom !== null)
      .sort((a, b) => a.vendegemRoom!.name!.localeCompare(b.vendegemRoom!.name!, 'hu'));

    this.mappedViewData = [
      ...mappedAndSorted,
      ...allMappedItems.filter(item => item.vendegemRoom === null)
    ];
  }

  getUnmappedVendegemRooms(): Room[] {
    const mappedVendegemExtIds = Object.values(this.currentMapping);
    return this.vendegemRooms.filter(room => !mappedVendegemExtIds.includes(String(room.id)));
  }
}

