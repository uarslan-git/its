import { Component, OnInit} from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Tutoring System for Programming';
  //name = new FormControl('');

/*   constructor(private mdService: MarkdownService) {}

  const markdown: string | undefined;

  ngOnInit(){
    this.markdown = this.mdService.compile("# Hallo");
  } */

  constructor(private client: HttpClient){}

  ngOnInit(): void {
    this.client.get<any>('http://127.0.0.1:8000/status').subscribe((data) =>  {
      console.log(data["message"]);
    });
  }
  

}
