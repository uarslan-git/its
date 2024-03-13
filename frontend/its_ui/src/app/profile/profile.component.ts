import { Component, AfterViewInit, EventEmitter, Output, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { EventShareService } from '../shared/services/event-share.service';
import { environment } from 'src/environments/environment';

import { DataTermsPopupComponent } from '../shared/components/data-terms-popup/data-terms-popup.component';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {

  @ViewChild('dataTermsPopupComponent', {static: true}) dataTermsPopupComponent!: DataTermsPopupComponent;
  showDataTermsPopup(){
    this.dataTermsPopupComponent.showPopup();
  }

  @ViewChild('consentCheckbox', {static: true}) consentCheckbox!: ElementRef

  @Output() profileAction: EventEmitter<string> = new EventEmitter<string>;

  apiUrl: string = environment.apiUrl;
  email: string = '';
  name: string = '';
  registeredDatetime: string = '';
  user: {email?: string, register_datetime?: any, settings?: any, enrolled_courses?: string[], roles?: string[]} = {};
  enrolledCourse: string = '';
  displayApiSettings: boolean = false;

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
          register_datetime: data.register_datetime,
          settings: data.settings,
          enrolled_courses: data.enrolled_courses,
          roles: data.roles
        };
        this.email = this.user.email!;
        this.name = this.user.email!.split("@")[0];
        this.registeredDatetime = this.user.register_datetime["local"];
        this.enrolledCourse = this.user.enrolled_courses![0];
        if(this.user.settings.dataCollection) {
          this.consentCheckbox.nativeElement.checked = true;
        }
        else {
          this.consentCheckbox.nativeElement.checked = false;
        }
        if(data.roles.includes("admin")){
          this.displayApiSettings = true;
        }
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

    updateSettings() {
      if(this.consentCheckbox.nativeElement.checked != this.user.settings.dataCollection) {
        this.user.settings.dataCollection = this.consentCheckbox.nativeElement.checked
        this.http.patch<any>(`${this.apiUrl}/users/me`, this.user, {withCredentials: true}).subscribe();
        sessionStorage.setItem('dataCollection', this.consentCheckbox.nativeElement.checked)
      }
    }

    saveApiUrl(url: string) {
      this.http.post(`${this.apiUrl}/feedback/set_llm_url`,{"url": url}, {withCredentials: true}).subscribe(
        (data) => {

        }
      );
    }
}