import { Component, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SyncRecord, SyncDetail } from 'src/app/models/sync';
import { SyncService } from 'src/app/services/sync.service';

@Component({
  selector: 'app-sync',
  templateUrl: './sync.component.html',
  styleUrls: ['./sync.component.css']
})
export class SyncComponent {

  @Input() accommodationId?: number;
  syncHistory: SyncRecord[] = [];
  selectedDetails: SyncDetail[] | null = null;

  constructor(
    private route: ActivatedRoute,
    private syncService: SyncService
  ) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.accommodationId = +id;
        this.loadSyncHistory();
      }
    });
  }

  loadSyncHistory(): void {
    this.syncService.getSyncHistory(this.accommodationId!).subscribe({
      next: (data) => {
        this.syncHistory = data;
        console.log(data)
      },
      error: (err) => {
        console.error('Hiba a szinkronizációs adatok betöltésekor:', err);
      }
    });
  }

  openDetailsModal(record: SyncRecord): void {
    this.selectedDetails = record.details;
  }

}