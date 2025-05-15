import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { RegistrationComponent } from './pages/registration/registration.component';
import { UserListComponent } from './components/users/user-list/user-list.component';
import { UserProfileComponent } from './components/users/user-profile/user-profile.component';
import { UserDetailsComponent } from './components/users/user-details/user-details.component';
import { ForgottenPasswordComponent } from './pages/forgotten-password/forgotten-password.component';
import { ConnectionsComponent } from './components/accomodation/connections/connections.component';
import { SyncComponent } from './components/sync/sync.component';
import { ConfigComponent } from './components/accomodation/config/config.component';
import { AccomodationListComponent } from './components/accomodation/accomodation-list/accomodation-list.component';
import { AccomodationProfileComponent } from './components/accomodation/accomodation-profile/accomodation-profile.component';
import { adminGuard, userDetailsGuard } from './components/security.components';


const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch:'full' },
  { path: 'users', component: UserListComponent, canActivate: [adminGuard] },
  {
    path: 'users/:id', 
    component: UserDetailsComponent, 
    canActivate: [userDetailsGuard],
    children: [
      { path: '', redirectTo: 'profil', pathMatch: 'full' },
      { path: 'profil', component: UserProfileComponent },
      {
        path: 'accommodations',
        component: AccomodationListComponent,
        children: [
          {
            path: ':id',
            children: [
              { path: '', redirectTo: 'profil', pathMatch: 'full' },
              { path: 'profil', component: AccomodationProfileComponent },
              { path: 'sync', component: SyncComponent },
              { path: 'config', component: ConfigComponent }
            ]
          }
        ]
      },

    ]
  },
  { path: 'login', component: LoginComponent },
  { path: 'registration', component: RegistrationComponent },
  { path: 'forgotten-password', component: ForgottenPasswordComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

export const routingComponents = [
  LoginComponent,
  ForgottenPasswordComponent,
  RegistrationComponent,
  UserListComponent,
  UserDetailsComponent,
  UserProfileComponent,
  ConnectionsComponent,
  ConfigComponent,
  SyncComponent,
  AccomodationListComponent,
  AccomodationProfileComponent
];
