import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { User } from '../../../models/user';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})
export class UserListComponent {
  users: User[] = [];
  filteredUsers: User[] = [];
  pageSize = 5;
  currentPage = 1;
  searchText = "";

  constructor(private userService: UserService, private router: Router) { }

  ngOnInit(): void {
    this.userService.listUsers().subscribe(users => {
      this.users = users;
      this.applyFilter();
    });
  }

  applyFilter(): void {
    this.filteredUsers = this.users.filter(user =>
      user.full_name.toLowerCase().includes(this.searchText.toLowerCase())
      ||
      user.username.toLowerCase().includes(this.searchText.toLowerCase())
      ||
      user.email.toLowerCase().includes(this.searchText.toLowerCase())
    );
    this.currentPage = 1;
  }

  get paginatedUsers(): User[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.filteredUsers.slice(start, start + this.pageSize);
  }

  changePage(page: number): void {
    this.currentPage = page;
  }

  goToUser(userId: number): void {
    this.router.navigate(['/users', userId]);
  }

  deactivateUser(userId: number): void {
    //TODO: deaktiválni a usert
  }

  get totalPages(): number[] {
    const count = Math.ceil(this.filteredUsers.length / this.pageSize);
    return Array(count).fill(0).map((_, i) => i + 1);
  }

}
