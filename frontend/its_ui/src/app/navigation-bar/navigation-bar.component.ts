import { Component, ElementRef, EventEmitter, Output, ViewChild } from '@angular/core';
import { EventShareService } from '../shared/services/event-share.service';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-navigation-bar',
  templateUrl: './navigation-bar.component.html',
  styleUrls: ['./navigation-bar.component.css']
})
export class NavigationBarComponent {

  @Output() profileButtonClicked: EventEmitter<string> = new EventEmitter<string>;

  @ViewChild('aboutPopup', {static: true}) aboutPopup!: ElementRef<HTMLDialogElement>

  aboutMarkdown: string = ''

  title: string = 'Tutoring System for Programming'
  task_name: string = ''

  constructor(
    private eventShareService: EventShareService,
    private httpClient: HttpClient,
    ){
      this.eventShareService.newTaskFetched$.subscribe(
        () => {
          this.task_name = sessionStorage.getItem("taskId")!
        }
      )
    }

  newTaskButtonClicked(direction: string){
    this.eventShareService.emitNewTaskEvent(direction);
  }

  emitProfileButtonClicked() {
    //this.eventShareService.emitProfileButtonClick();
    this.profileButtonClicked.emit("profileRequest")
  }

  openAboutPopup() {
    this.httpClient.get<any>(`${environment.apiUrl}/info/about`)
        .subscribe(data => {
          this.aboutMarkdown = data.about_markdown;
        });
    this.aboutPopup.nativeElement.showModal();
  }
}
