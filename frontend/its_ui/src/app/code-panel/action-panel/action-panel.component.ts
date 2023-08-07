import { Component, Output, EventEmitter } from '@angular/core';
import { EventShareService } from 'src/app/shared/services/event-share.service';
import { v4 as uuidv4 } from 'uuid'

@Component({
  selector: 'app-action-panel',
  templateUrl: './action-panel.component.html',
  styleUrls: ['./action-panel.component.css']
})
export class ActionPanelComponent {

  @Output() submitEvent : EventEmitter<string> = new EventEmitter<string>();
  submissionId: string = '';

  constructor(private eventShareService: EventShareService){}

  //Submit Button
  submitButtonClicked() {
    this.submissionId = uuidv4()
    this.submitEvent.emit(this.submissionId);
    this.eventShareService.emitSubmitButtonClick(this.submissionId);
  }
}
