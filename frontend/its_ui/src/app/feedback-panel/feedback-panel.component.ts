import { Component } from '@angular/core';
import { Subscription } from 'rxjs';
import { EventShareService } from '../shared/services/event-share.service';

@Component({
  selector: 'app-feedback-panel',
  templateUrl: './feedback-panel.component.html',
  styleUrls: ['./feedback-panel.component.css']
})
export class FeedbackPanelComponent {

  private subscription: Subscription;
  code_language: string = 'python';
  feedback: string = '';

  constructor(private eventShareService: EventShareService){
    this.subscription = this.eventShareService.submitButtonClick$.subscribe(() => {
      this.feedback = 'Code submitted, waiting for feedback...';
    });
  }


  ngOnDestroy() {
    this.subscription.unsubscribe();
  }
}
