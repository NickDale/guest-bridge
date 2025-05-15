import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs/internal/Subscription';
import { AuthService } from 'src/app/services/authentication.service';

@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css']
})
export class TopBarComponent {
  username?: string;
  isLoggedIn: boolean = false;
  private authSubscription?: Subscription;
  
  constructor(
    private router: Router,
    private authService: AuthService
  ) { }

  ngOnInit(): void {
   // this.init();
    this.authSubscription = this.authService.loggedIn$.subscribe(loggedIn => {
      this.isLoggedIn = loggedIn;
      this.username = loggedIn ? this.authService.getUserName() : undefined;
    });
  }

  ngOnDestroy(): void {
    this.authSubscription?.unsubscribe();
  }

  navigateHome(): void {
    this.router.navigate([this.isLoggedIn ? '/users' : '/']);
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  init(){
    this.isLoggedIn = false;
    this.username = undefined; 
  }
}
