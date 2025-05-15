import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { User } from 'src/app/models/user';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-user-details',
  templateUrl: './user-details.component.html',
  styleUrls: ['./user-details.component.css']
})
export class UserDetailsComponent {

  user: User | undefined;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      let userId = +params.get('id')!;
      this.userService.getUserById(userId).subscribe(user => {
        this.user = user

        if (!this.user) {
          //this.router.navigate(['/users']);
          this.router.navigate(['../', { id: userId }], { relativeTo: this.route })
          return;
        }
        console.log("set selected user")
        console.log(this.user)
        this.userService.setSelectedUser(this.user);
      })
    });
  }

}
