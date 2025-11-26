import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { isAdmin } from 'src/app/services/security.components';
import { AuthService } from 'src/app/services/authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  passwordFieldType: string = 'password';
  errorMessage = '';

  loginForm!: FormGroup;

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  get loginFormCtrl() {
    return this.loginForm.controls;
  }

  ngOnInit(): void {
    this.loginForm = new FormGroup({
      username: new FormControl('', Validators.required),
      password: new FormControl('', [
        Validators.required,
        Validators.minLength(4)
      ])
    });
  }

  togglePasswordVisibility(): void {
    console.log(this.passwordFieldType)
    if (this.passwordFieldType === 'password') {
      this.passwordFieldType = 'text';
    } else {
      this.passwordFieldType = 'password';
    }
  }

  onSubmit() {
    this.errorMessage = '';
    const { username, password } = this.loginForm.value;
    this.authService.login(username, password).subscribe({
      next: success => {
        const user = this.authService.getUser();
        if (!user) {
          this.router.navigate([`/login`]);
        } else {
          let navigateTo = isAdmin(user) ? ['/users'] : ['/users', user.id];
          this.router.navigate(navigateTo).then(success => {
            console.log('Navigáció sikeres?', success);
          })
        }
      },
      error: error => {
        console.error('Hibás login');
        if (error.status === 401 || error.status === 403) {
          this.errorMessage = 'Hibás belépési adatok. Kérjük, ellenőrizze felhasználónevét és jelszavát. Vagy vegye fel a kapcsolatot az üzemeltetővel';
        } else {
          alert(`Hiba: ${error.error.detail}`);
        }
        this.loginForm.reset();
      }
    });
  }
}


