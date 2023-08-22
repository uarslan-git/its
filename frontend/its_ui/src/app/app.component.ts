import { Component, OnInit, } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Tutoring System for Programming';
  pageName = 'loginView'
  //name = new FormControl('');


  constructor(private client: HttpClient){}

  ngOnInit(): void {
    this.client.get<any>('http://127.0.0.1:8000/status').subscribe((data) =>  {
      console.log(data["message"]);
    });
  }

  setView(status: string) {
    switch (status) {
      case 'loggedIn':
          this.pageName = 'tutoringView';
          break;
      case 'loggedOut':
          this.pageName = 'loginView';
          break;
      default:
        this.pageName = 'loginView'
          console.log("Invalid View request");
          break;
  }
  }
  
}
