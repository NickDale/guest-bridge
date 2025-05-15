import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css']
})
export class TopBarComponent {
  isLoggedIn = false; 
  username: string | null = null;

  //TODO: finish
  constructor(private router: Router) {
    this.username = localStorage.getItem('username') ?? null;
    this.isLoggedIn = !!this.username;
  }

  navigateHome(): void {
    if (this.isLoggedIn) {
      this.router.navigate(['/users']); // vagy ['/users', id] később
    } else {
      this.router.navigate(['/']);
    }
  }

  logout(): void {
    localStorage.clear();
    this.router.navigate(['/login']);
  }
}
