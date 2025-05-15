import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Accomodation } from 'src/app/models/accommodation';
import { AccommodationService } from 'src/app/services/accommodation.service';

@Component({
  selector: 'app-accomodation-list',
  templateUrl: './accomodation-list.component.html',
  styleUrls: ['./accomodation-list.component.css']
})
export class AccomodationListComponent {

  accommodations: Accomodation[] = [];
  filteredAccommodations: Accomodation[] = [];
  pageSize = 3;
  currentPage = 1;
  searchText = "";
  selectedAccommodationId?: number;

  constructor(
    private accommodationService: AccommodationService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
     this.accommodationService.listAccommodations().subscribe(accommodations => {
      this.accommodations = accommodations
      this.applyFilter();
    });
    this.applyFilter();
  }

  applyFilter(): void {
    this.filteredAccommodations = this.accommodations.filter(a =>
      a.name.toLowerCase().includes(this.searchText.toLowerCase())
      ||
      a.address.toLowerCase().includes(this.searchText.toLowerCase())
    );
  }


  get pagedAccomodations(): Accomodation[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.filteredAccommodations.slice(start, start + this.pageSize);
  }
  get totalPages(): number[] {
    const count = Math.ceil(this.filteredAccommodations.length / this.pageSize);
    return Array(count).fill(0).map((_, i) => i + 1);
  }

  changePage(page: number): void {
    this.currentPage = page;
  }

  openModal(accommodationId: number): void {
    console.log("selected: " + accommodationId)
    this.selectedAccommodationId = accommodationId;
  }

  openDetail(id: number) {
    this.selectedAccommodationId = id;
    console.log("navigate..... and selectedAccommodationId ="+this.selectedAccommodationId)
    this.router.navigate([id, 'profil'], { relativeTo: this.route });
  }

}
