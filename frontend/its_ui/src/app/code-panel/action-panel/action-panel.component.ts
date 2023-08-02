import { Component, Output, EventEmitter } from '@angular/core';
import { EventShareService } from 'src/app/shared/services/event-share.service';

@Component({
  selector: 'app-action-panel',
  templateUrl: './action-panel.component.html',
  styleUrls: ['./action-panel.component.css']
})
export class ActionPanelComponent {

  @Output() submitEvent : EventEmitter<void> = new EventEmitter();

  constructor(private eventShareService: EventShareService){}

  //Submit Button
  submitButtonClicked() {
    this.submitEvent.emit();
    this.eventShareService.emitSubmitButtonClick();
  }
}
