import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { isAdmin } from 'src/app/components/security.components';
import { AuthService } from 'src/app/services/authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username = '';
  password = '';

  constructor(
    private authService: AuthService,
    private router: Router) { }

  onSubmit() {
    this.authService.login(this.username, this.password).subscribe(success => {
      if (success) {
        const user = this.authService.getUser();
        if (!user) {
          this.router.navigate([`/login`]);
        } else {
          let navigateTo = isAdmin(user) ? ['/users'] : ['/users', user.id];
          this.router.navigate(navigateTo).then(success => {
            console.log('Navigáció sikeres?', success);
          })
        }
      } else {
        // this.loginError = 'Hibás felhasználónév vagy jelszó!';
        alert('Hibás bejelentkezés!');
      }
    });



  }
}


