import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs/internal/Subscription';
import { AuthService } from 'src/app/services/authentication.service';
import { isAdmin } from 'src/app/services/security.components';

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
    this.authSubscription = this.authService.loggedIn$.subscribe(loggedIn => {
      this.isLoggedIn = loggedIn;
      this.username = loggedIn ? this.authService.getUserName() : undefined;
    });
  }

  ngOnDestroy(): void {
    this.authSubscription?.unsubscribe();
  }

  navigateHome(): void {
    if (this.isLoggedIn) {
      const user = this.authService.getUser();
      if (user) {
        let navigateTo = isAdmin(user) ? ['/users'] : ['/users', user.id];
        this.router.navigate(navigateTo)
      }
    } else {
      this.router.navigate(['/']);
    }
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  init() {
    this.isLoggedIn = false;
    this.username = undefined;
  }
}
