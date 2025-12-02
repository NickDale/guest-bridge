import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule, routingComponents } from './app-routing.module';
import { AppComponent } from './app.component';
import { TopBarComponent } from './components/top-bar/top-bar.component';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { AccomodationDetailComponent } from './components/accomodation/accomodation-detail/accomodation-detail.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { ErrorInterceptor } from './interceptors/error.interceptor';
import { UserRegistrationFormComponent } from './components/users/user-registration-form/user-registration-form.component';
import { AccomodationRegistrationFormComponent } from './components/accomodation/accomodation-registration-form/accomodation-registration-form.component';
import { PasswordChangeComponent } from './components/users/password-change/password-change.component';
import { SyncStartComponent } from './components/accomodation/sync/sync-start/sync-start.component';
@NgModule({
  declarations: [
    AppComponent,
    TopBarComponent,
    routingComponents,
    AccomodationDetailComponent,
    UserRegistrationFormComponent,
    AccomodationRegistrationFormComponent,
    PasswordChangeComponent,
    SyncStartComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatProgressSpinnerModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatToolbarModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ErrorInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
