import { Component, AfterViewInit, EventEmitter, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { EventShareService } from '../shared/services/event-share.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {

  @Output() profileAction: EventEmitter<string> = new EventEmitter<string>;

  apiUrl: string = 'http://127.0.0.1:8000';
  email: string = '';
  name: string = '';
  user: {email?: string} = {};

  constructor(private http: HttpClient,
    private eventShareService: EventShareService) {
/*       this.eventShareService.profileButtonClick$.subscribe((data) => {
        this.show_profile();
      }); */
    }

    ngAfterViewInit() {
      this.show_profile()
    }

    show_profile() {
      this.http.get<any>(`${this.apiUrl}/users/me`, {"withCredentials": true}).subscribe(
        (data)  => {
        this.user = {
          email: data.email,
        };
        this.email = this.user.email!;
        this.name = this.user.email!.split("@")[0];
      });
    }

    logout(){
      this.http.post(`${this.apiUrl}/auth/jwt/logout`,{}, {withCredentials: true}).subscribe();
      console.log("logged out!");
      this.profileAction.emit('loggedOut');
    }

    closeProfile() {
      console.log("close profile!");
      this.profileAction.emit('closedProfile');
    }
}

