import { Component, ElementRef, ViewChild } from '@angular/core';
import { Subscription } from 'rxjs';
import { EventShareService } from '../shared/services/event-share.service';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-feedback-panel',
  templateUrl: './feedback-panel.component.html',
  styleUrls: ['./feedback-panel.component.css']
})
export class FeedbackPanelComponent {

  @ViewChild("taskSolvedDialog", {static: true}) taskSolvedDialog!: ElementRef<HTMLDialogElement>;

  private submitSubscription: Subscription;
  private testReadySubscription: Subscription;
  private newTaskSubscription: Subscription;
  private codeRunSubscription: Subscription;
  private codeRunReadySubscription: Subscription;

  code_language: string = 'python';
  feedback_markdown: string = '';
  feedback:  { test_results?: Array<any>; task_id?: string; submission_id?: string; valid_solution?: boolean, output?: boolean} = {};
  submissionId: string = '';
  

  constructor(
    private eventShareService: EventShareService,
    private client: HttpClient,){
    this.submitSubscription = this.eventShareService.submitButtonClick$.subscribe((data) => {
      this.feedback_markdown = 'Code submitted, waiting for feedback...';
    });
    this.testReadySubscription = this.eventShareService.testReady$.subscribe((data) => {
      const submissionId = data
      this.fetchFeedback(submissionId);
    });
    this.newTaskSubscription = this.eventShareService.newTaskEvent$.subscribe(() => {
      this.feedback_markdown = '';
    });
    this.codeRunSubscription = this.eventShareService.runButtonClick$.subscribe(
      () => {
        this.feedback_markdown = 'Code Experiment started, waiting for results...'
      }
    );
    this.codeRunReadySubscription = this.eventShareService.codeRunReady$.subscribe(
      (run_id) => {
        this.fetchRunExperiment(run_id);
    })
  }

  fetchFeedback(submission_id: string) {
    const submission_url = `${environment.apiUrl}/feedback/${submission_id}`
    this.client.get<any>(submission_url, ).subscribe((data) => { 
      this.feedback = {
        test_results: data.test_results,
        task_id: data.task_unique_name,
        submission_id: data.submission_id,
        valid_solution: data.valid_solution,
    };
    this.feedback_markdown = this.renderTestResults(this.feedback["test_results"]!, this.feedback["task_id"]!);
    if(this.feedback["valid_solution"]) {
      this.openValidSolutionDialog();
    }
    //this.evaluateFeedback(this.feedback["valid_solution"]!);
    //this.feedback_string = JSON.stringify(this.feedback);
  });
  }

  renderTestResults(feedback_array: Array<any>, task_name: string) {
    var feedback_markdown = `# Feedback for task ${task_name}\n`;
    for (var test_obj of feedback_array) {
      feedback_markdown += "## " + test_obj["test_name"] + "\n";
      feedback_markdown += test_obj["message"];
      feedback_markdown += '\n';
    }
    return(feedback_markdown);
  }

  fetchRunExperiment(runId: string) {
    const submission_url = `${environment.apiUrl}/feedback/${runId}`
    this.client.get<any>(submission_url, ).subscribe((data) => { 
      this.feedback = {
        output: data.run_output,
        task_id: data.task_unique_name,
    };
    this.feedback_markdown = data.run_output;
  });
  }

  openValidSolutionDialog()
  {
    this.taskSolvedDialog.nativeElement.showModal();
  }

  actOnValidSolution(action: string) {
    if (action == "stay") {
      this.taskSolvedDialog.nativeElement.close();
    }
    else if (action == "next task") {
      this.eventShareService.emitNewTaskEvent('personal');
      this.taskSolvedDialog.nativeElement.close();
    }
  }

  ngOnDestroy() {
    this.submitSubscription.unsubscribe();
    this.testReadySubscription.unsubscribe();
    this.newTaskSubscription.unsubscribe();
    this.codeRunSubscription.unsubscribe();
    this.codeRunReadySubscription.unsubscribe();
  }
}
