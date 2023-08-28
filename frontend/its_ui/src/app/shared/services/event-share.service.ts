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
  private submitButtonClickSubject = new Subject<string>();
  submitButtonClick$ = this.submitButtonClickSubject.asObservable();

  emitSubmitButtonClick(submissionId: string) {
    this.submitButtonClickSubject.next(submissionId);
  }

  // Tests ready Event
  private testReadySubject = new Subject<void>();
  testReady$ = this.testReadySubject.asObservable();

  emitTestReadyEvent() {
    this.testReadySubject.next();
  }

  //New Task Event
  private newTaskEventSubject = new Subject<void>();
  newTaskEvent$ = this.newTaskEventSubject.asObservable();

  emitNewTaskEvent() {
    this.newTaskEventSubject.next();
  }

  //Profile Button Click
  private profileButtonClickSubject = new Subject<void>();
  profileButtonClick$ = this.profileButtonClickSubject.asObservable();

  emitProfileButtonClick() {
    this.profileButtonClickSubject.next();
  }

}
