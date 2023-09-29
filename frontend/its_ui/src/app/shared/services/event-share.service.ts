/*
 * This Service is used to share events and data between not dierctly 
 * reated (paret - child) components. Directly related components
 * share their events using the @Input/Output Pattern
 */
import { Injectable } from '@angular/core';
import {Subject} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EventShareService {

  constructor() { }

  //Submit button click
  private submitButtonClickSubject = new Subject<void>();
  submitButtonClick$ = this.submitButtonClickSubject.asObservable();

  emitSubmitButtonClick() {
    this.submitButtonClickSubject.next();
  }

  // Tests ready Event
  private testReadySubject = new Subject<string>();
  testReady$ = this.testReadySubject.asObservable();

  emitTestReadyEvent(submissionId: string) {
    this.testReadySubject.next(submissionId);
  }

  //run button click
  private runButtonClickSubject = new Subject<void>();
  runButtonClick$ = this.runButtonClickSubject.asObservable();

  emitRunButtonClick() {
    this.runButtonClickSubject.next();
  }

  // Code Run ready Event
  private codeRunReadySubject = new Subject<string>();
  codeRunReady$ = this.codeRunReadySubject.asObservable();

  emitCodeRunReadyEvent(codeRunId: string) {
    this.codeRunReadySubject.next(codeRunId);
  }

  //New Task Event
  private newTaskEventSubject = new Subject<string>();
  newTaskEvent$ = this.newTaskEventSubject.asObservable();

  emitNewTaskEvent(direction: string) {
    this.newTaskEventSubject.next(direction);
  }

  //View Change Event
  private viewChangeSubject = new Subject<string>();
  viewChange$ = this.viewChangeSubject.asObservable();

  emitViewChange(view: string) {
    this.viewChangeSubject.next(view);
  }

}
