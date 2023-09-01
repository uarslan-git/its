import { Component, EventEmitter, Output } from '@angular/core';
import { EventShareService } from '../shared/services/event-share.service';
import { DataShareService } from '../shared/services/data-share.service';

@Component({
  selector: 'app-navigation-bar',
  templateUrl: './navigation-bar.component.html',
  styleUrls: ['./navigation-bar.component.css']
})
export class NavigationBarComponent {

  @Output() profileButtonClicked: EventEmitter<string> = new EventEmitter<string>;

  title: string = 'Tutoring System for Programming'
  task_name: string = ''

  constructor(
    private eventShareService: EventShareService,
    private dataShareService: DataShareService){
      this.dataShareService.taskIdShare$.subscribe(
        (data) => {
          this.task_name = data
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
}
