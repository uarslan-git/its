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

  //New Task Event
  private newTaskEventSubject = new Subject<void>();
  newTaskEvent$ = this.newTaskEventSubject.asObservable();

  emitNewTaskEvent() {
    this.newTaskEventSubject.next();
  }

  //View Change Event
  private viewChangeSubject = new Subject<string>();
  viewChange$ = this.viewChangeSubject.asObservable();

  emitViewChange(view: string) {
    this.viewChangeSubject.next(view);
  }

}
