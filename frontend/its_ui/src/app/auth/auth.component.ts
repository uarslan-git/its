import { Component, EventEmitter, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { EventShareService } from '../shared/services/event-share.service';


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
  apiUrl = 'http://127.0.0.1:8000';

  @Output() loginEvent : EventEmitter<string> = new EventEmitter<string>();
  loginStatus: string = 'none';

  registering: boolean = false;

  constructor(private http: HttpClient,
              private eventShareService: EventShareService) {
                eventShareService.profileButtonClick$.subscribe((data) => {
                  this.show_profile();
                });
              }

  login(username: string, password: string): void {
    // unfortunatley, the fastapi-users package requres logins to be FormData and not JSON.
    const formData = new FormData()
    formData.append('username', `${username}@anonym.de`); //At some later point we may want to prefer e-mail based login
    formData.append('password', password);

    this.http.post<Response>(`${this.apiUrl}/auth/jwt/login`, formData, { withCredentials: true, observe: 'response' }).subscribe(
      response => {
          // Handle successful login, e.g., store the token in local storage
          // localStorage.setItem('token', response.token);
          this.loginStatus = "loggedIn";
          this.emitLoginEvent();
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

  register(username: string, password: string): void {
    const body = {"email": `${username}@anonym.de`,
    "password": password };
    this.http.post<AuthResponse>(`${this.apiUrl}/auth/register`, body).subscribe(
      response => {
        if (response.token) {
          // Handle successful registration, similar to login
          localStorage.setItem('token', response.token);
          console.log(response.message);
        }
      },
      error => {
        console.error('Registration error:', error);
      }
    );
  }

  show_profile() {
    this.http.get(`${this.apiUrl}/users/me`, {"withCredentials": true}).subscribe(
      response => {
        console.log(response)
      }
    )
  }

  setRegistering(registering: boolean){
    this.registering = registering;
  }

}
