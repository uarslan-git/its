import { Component } from '@angular/core';
import { EventShareService } from '../shared/services/event-share.service';

@Component({
  selector: 'app-navigation-bar',
  templateUrl: './navigation-bar.component.html',
  styleUrls: ['./navigation-bar.component.css']
})
export class NavigationBarComponent {

  title: string = 'Tutoring System for Programming'

  constructor(private eventShareService: EventShareService){}

  newTaskButtonClicked(){
    this.eventShareService.emitNewTaskButtonClick();
  }

}
