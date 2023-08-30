import { Component, Renderer2,  AfterViewChecked, AfterViewInit, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { DatePipe } from '@angular/common';

//Prism
import { FormBuilder } from '@angular/forms'
import { fromEvent, Subscription } from 'rxjs';
import { PrismHighlightService } from '../shared/services/prism-highlight.service'
import { HttpClient } from '@angular/common/http';

import { DataShareService } from '../shared/services/data-share.service';
import { EventShareService } from '../shared/services/event-share.service';
import { CodeEditorComponent } from './code-editor/code-editor.component';


@Component({
  selector: 'app-code-panel',
  templateUrl: './code-panel.component.html',
  styleUrls: ['./code-panel.component.css'],
})
export class CodePanelComponent {

  submitted_code: string = ''
  code_language = 'python';
  @ViewChild(CodeEditorComponent)
  codeEditorComponent!: CodeEditorComponent;


  //Submit Button
  submitButtonClicked(submissionId: string) {
    this.submitted_code = this.codeEditorComponent.contentControl;
    this.client.post<any>('http://127.0.0.1:8000/code_submit', 
          {task_unique_name: this.current_task_id, code: this.submitted_code, 
            log: "True", submission_id: submissionId,
            submission_time: this.datePipe.transform((new Date), 'MM/dd/yyyy h:mm:ss')},
            {withCredentials: true}).subscribe((data) => {
              this.eventShareService.emitTestReadyEvent();
    });
  }


  taskIdSubscription: Subscription;
  current_task_id: string = "";

  constructor(
/*       private prismService: PrismHighlightService,
      private fb: FormBuilder,
      private renderer: Renderer2, */
      private client: HttpClient,
      private dataShareService: DataShareService,
      private eventShareService: EventShareService,
      public datePipe: DatePipe,
    ) {
      this.taskIdSubscription = this.dataShareService.taskIdShare$.subscribe(
        (data) => {this.current_task_id = data;
                  console.log(this.current_task_id);
                  this.getCurrentAttemptState();}
      );
    }

    // Tracking Users Coding process

    currentAttemptId!: string;
    contentReloaded: boolean = false;

    getCurrentAttemptState() {
      this.client.get<any>(`http://127.0.0.1:8000/attempt/get_state/${this.current_task_id}`, {withCredentials: true}).subscribe(
        (data) => {
          console.log(data.attempt_id)
          this.currentAttemptId = data.attempt_id;
          this.codeEditorComponent.form.setValue({'content': data.code});
          this.contentReloaded = true;
        }
      )
    }

    recordChanges(newContent: string) {
      if (!this.contentReloaded) {
        const body = {
          'attempt_id': this.currentAttemptId,
          'code': newContent, 
          'state_datetime': this.datePipe.transform((new Date), 'MM/dd/yyyy h:mm:ss'), //TODO: Use correct time zones
          'submission_id': ''};
        this.client.post<any>('http://127.0.0.1:8000/attempt/log', body, {withCredentials: true}).subscribe(
          () => {
            console.log("State logged");
          }
        )
      }
        this.contentReloaded = false;
    }
}
