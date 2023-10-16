import { Component, ElementRef, EventEmitter, Output, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { EventShareService } from '../shared/services/event-share.service';
import { DatetimeService } from '../shared/services/datetime.service';

import { environment } from 'src/environments/environment';
import { DataTermsPopupComponent } from '../shared/components/data-terms-popup/data-terms-popup.component';

interface AuthResponse {
  message: string;
  token?: string;
}

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent {

  @ViewChild('dataTermsPopupComponent', { static: false }) dataTermsPopupComponent!: DataTermsPopupComponent;
  @ViewChild('consentCheckboxYes', {static: false}) consentCheckboxYes!: ElementRef;
  @ViewChild('consentCheckboxNo', {static: false}) consentCheckboxNo!: ElementRef;
  //TODO: Fetch availiable courses directly from database.
  @ViewChild('courseSelection', {static: false}) courseSelection!: ElementRef;

  //showDataTermPopup: boolean = false;
  showDataTermPopup() {
    this.dataTermsPopupComponent!.showPopup();
  }

  apiUrl = environment.apiUrl;
  timer: any;

  @Output() loginEvent : EventEmitter<string> = new EventEmitter<string>();
  loginStatus: string = 'none';

  registering: boolean = false;

  constructor(private http: HttpClient,
              private eventShareService: EventShareService,
              private datetimeService: DatetimeService) {}

  login(username: string, password: string): void {
    // unfortunatley, the fastapi-users package requres logins to be FormData and not JSON.
    const formData = new FormData()
    formData.append('username', `${username}@anonym.de`); //At some later point we may want to prefer e-mail based login
    formData.append('password', password);

    this.http.post<any>(`${this.apiUrl}/auth/jwt/login`, formData, { withCredentials: true}).subscribe(
      () => {
          // Handle successful login
          this.loginStatus = "loggedIn";
          this.emitLoginEvent();
          this.timer = setTimeout(
            () => {
              this.loginStatus = 'LoggedOut';
              this.eventShareService.emitViewChange(this.loginStatus);
              alert("You have been automatically logged out, since your authentification token has expired. However you can just log back in, your progress is stored.")
            }
            , 6400000);
           this.retrieveSessionSettings();
      },
      error => {
        console.error('Login error:', error);
        alert("Login not successful. Please provide valid credentials and ensure a proper connection.")
      }
    );
  }

  emitLoginEvent() {
    this.loginEvent.emit(this.loginStatus);
  }

  register(username: string, password: string, dataCollectionConsent: boolean, courseSelection: string): void {
    if(!this.consentCheckboxNo.nativeElement.checked && !this.consentCheckboxYes.nativeElement.checked){
      window.alert("Please select (Yes/No) whether we can use your data for scientific purposes.")
      return;
    }
    if(courseSelection=='none') {
      window.alert("Please select a course.")
      return;
    }
    const body = {"email": `${username}@anonym.de`,
                  "password": password, "tasks_completed": [], "tasks_attempted": [], 
                  "enrolled_courses": [courseSelection], "courses_completed": [],
                  "register_datetime": this.datetimeService.datetimeNow(),
                  "settings": {"dataCollection": dataCollectionConsent}
                };
    this.http.post<AuthResponse>(`${environment.apiUrl}/auth/register`, body).subscribe(
      response => {
          // Handle successful registration
          this.setRegistering(false);
      },
      error => {
        console.error('Registration error:', error);
        alert("Registration not successful. Probably the user already exists.")
      }
    );
  }

  setRegistering(registering: boolean){
    this.registering = registering;
  }

  retrieveSessionSettings() {
    this.http.get<any>(`${this.apiUrl}/users/me`, {withCredentials: true}).subscribe(
      (data) => {
        const settings = data.settings
        //for (var key in Object.keys(settings)) {
          for (const key in settings) {
            sessionStorage.setItem(key, settings[key]);
        }
      }
    )
  }
}
