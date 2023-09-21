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
import { DatetimeService } from '../shared/services/datetime.service';

import { environment } from 'src/environments/environment';


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
  submitButtonClicked() {
    this.submitted_code = this.codeEditorComponent.contentControl;
    this.client.post<any>(`${environment.apiUrl}/code_submit`, 
          {task_unique_name: this.current_task_id, code: this.submitted_code, 
            log: "True",
            submission_time: this.datetimeService.datetimeNow()
          },
            {withCredentials: true}).subscribe((data) => {
              this.recordChanges(this.submitted_code, data.submission_id);
              this.eventShareService.emitTestReadyEvent(data.submission_id);
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
      private datetimeService: DatetimeService,
    ) {
      this.taskIdSubscription = this.dataShareService.taskIdShare$.subscribe(
        (data) => {this.current_task_id = data;
                  this.getCurrentAttemptState();}
      );
    }

    // Tracking Users Coding process, also functionality to save and restore attempts.

    currentAttemptId!: string;
    contentReloaded: boolean = false;

    getCurrentAttemptState() {
      this.client.get<any>(`${environment.apiUrl}/attempt/get_state/${this.current_task_id}`, {withCredentials: true}).subscribe(
        (data) => {
          this.currentAttemptId = data.attempt_id;
          this.codeEditorComponent.form.setValue({'content': data.code});
          this.contentReloaded = true;
        }
      )
    }

    recordChanges(newContent: string, submissionId: string='') {
      if ((!this.contentReloaded) || (this.current_task_id=='course completed')) {
        const body = {
          'attempt_id': this.currentAttemptId,
          'code': newContent, 
          'state_datetime': this.datetimeService.datetimeNow(),
          'submission_id': submissionId};
        this.client.post<any>(`${environment.apiUrl}/attempt/log`, body, {withCredentials: true}).subscribe(
          () => {
            console.log("State logged");
          }
        )
      }
        this.contentReloaded = false;
    }
}
