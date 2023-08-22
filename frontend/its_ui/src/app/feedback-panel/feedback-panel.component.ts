import { Component } from '@angular/core';
import { Subscription } from 'rxjs';
import { EventShareService } from '../shared/services/event-share.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-feedback-panel',
  templateUrl: './feedback-panel.component.html',
  styleUrls: ['./feedback-panel.component.css']
})
export class FeedbackPanelComponent {

  private submitSubscription: Subscription;
  code_language: string = 'python';
  feedback_markdown: string = '';
  feedback:  { test_results?: Array<any>; task_id?: string; submission_id?: string} = {};
  submissionId: string = '';

  private testReadySubscription: Subscription;

  constructor(
    private eventShareService: EventShareService,
    private client: HttpClient,){
    this.submitSubscription = this.eventShareService.submitButtonClick$.subscribe((data) => {
      this.submissionId = data;
      this.feedback_markdown = 'Code submitted, waiting for feedback...';
    });

    this.testReadySubscription = this.eventShareService.testReady$.subscribe((data) => {
      this.fetch_feedback(this.submissionId);
    });
  }

  fetch_feedback(submission_id: string) {
    const submission_url = `http://127.0.0.1:8000/feedback/${submission_id}`
    this.client.get<any>(submission_url, ).subscribe((data) => { 
      this.feedback = {
        test_results: data.test_results,
        task_id: data.task_id,
        submission_id: data.submission_id,
    };
    this.feedback_markdown = this.process_feedback(this.feedback["test_results"]!, this.feedback["task_id"]!);
    console.log(data);
    //this.feedback_string = JSON.stringify(this.feedback);
  });
  }

  process_feedback(feedback_array: Array<any>, task_name: string) {
    var feedback_markdown = `# Feedback for task ${task_name}\n`;
    for (var test_obj of feedback_array) {
      feedback_markdown += "## " + test_obj["test_name"] + "\n";
      feedback_markdown += test_obj["message"];
      feedback_markdown += '\n';
    }
    return(feedback_markdown);
  }

  ngOnDestroy() {
    this.submitSubscription.unsubscribe();
    this.testReadySubscription.unsubscribe();
  }
}