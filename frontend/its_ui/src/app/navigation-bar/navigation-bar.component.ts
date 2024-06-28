import { Component, ElementRef, EventEmitter, Output, ViewChild, Input } from '@angular/core';
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
  @Output() homeButtonClicked: EventEmitter<string> = new EventEmitter<string>;
  @Output() courseSettingButtonClicked: EventEmitter<string> = new EventEmitter<string>;

  @ViewChild('aboutPopup', {static: true}) aboutPopup!: ElementRef<HTMLDialogElement>

  aboutMarkdown: string = '';

  apiUrl: string = environment.apiUrl;
  user_name: string = "INVALID_EMAIL";
  title: string = 'Tutoring System for Programming';
  task_name: string = '';
  course?: any;

  display_elements: Set<string> = new Set(); 
  _currentPageName?: string

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

  @Input() set currentPageName(pageName: string){
    this._currentPageName = pageName
    this.updateDisplayElements()
  }

  updateDisplayElements(){
    if(this._currentPageName == "tutoringView"){
      this.display_elements.add("taskSelection")
      this.display_elements.add("courseSettings")
    }
  }

  ngAfterViewInit() {
    this.show_profile()
  }

  show_profile() {
    this.httpClient.get<any>(`${this.apiUrl}/users/me`, {"withCredentials": true}).subscribe(
      (data)  => {
        this.user_name = data.email!.split("@")[0];
    });
  }


  newTaskButtonClicked(direction: string){
    this.eventShareService.emitNewTaskEvent(direction);
  }

  emitProfileButtonClicked() {
    //this.eventShareService.emitProfileButtonClick();
    this.profileButtonClicked.emit("profileRequest")
  }

  emitHomeButtonClicked() {
    //this.eventShareService.emitProfileButtonClick();
    this.homeButtonClicked.emit("homeRequest")
  }

  openAboutPopup() {
    this.httpClient.get<any>(`${environment.apiUrl}/info/about`)
        .subscribe(data => {
          this.aboutMarkdown = data.about_markdown;
        });
    this.aboutPopup.nativeElement.showModal();
  }

  emitCourseSettingsRequested() {
    this.courseSettingButtonClicked.emit("courseSettingsRequest")
  }
}