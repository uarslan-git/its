import { Component, OnInit, } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { EventShareService } from './shared/services/event-share.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Tutoring System for Programming';
  pageName = 'loginView'
  originPage = ''
  initTask?: string;
  //name = new FormControl('');

  constructor(private client: HttpClient,
    eventShareService: EventShareService){
      eventShareService.viewChange$.subscribe(
        (status) => {
          this.setView(status);
        }
      );
  }

  ngOnInit(): void {
    this.client.get<any>(`${environment.apiUrl}/status`).subscribe((data) =>  {
      console.log(data["message"]);
    });
  }

  setView(status: string) {
    switch (status) {
      case 'loggedIn':
          this.pageName = 'welcomePage';
          break;
      case 'loggedOut':
          this.pageName = 'loginView';
          break;
      case 'courseSelected':
          this.pageName = 'tutoringView';
          break;
      case 'closedProfile':
        this.initTask = sessionStorage.getItem("taskId")!;
        this.pageName = this.originPage;
        break;
      case 'profileRequest':
        this.originPage = this.pageName
        this.pageName = 'profileView';
        break;
      default:
        this.pageName = 'loginView'
          console.log("Invalid View request");
          break;
    }
  }
}
