import { Component, AfterViewInit, EventEmitter, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { EventShareService } from '../shared/services/event-share.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {

  @Output() profileAction: EventEmitter<string> = new EventEmitter<string>;

  apiUrl: string = environment.apiUrl;
  email: string = '';
  name: string = '';
  registeredDatetime: string = '';
  user: {email?: string, register_datetime?: any} = {};

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
          register_datetime: data.register_datetime
        };
        this.email = this.user.email!;
        this.name = this.user.email!.split("@")[0];
        this.registeredDatetime = this.user.register_datetime["local"];
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

