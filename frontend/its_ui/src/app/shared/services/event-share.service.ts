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

  //New Task Request from User
  private newTaskButtonClickSubject = new Subject<void>();
  newTaskButtonClick$ = this.newTaskButtonClickSubject.asObservable();

  emitNewTaskButtonClick() {
    this.newTaskButtonClickSubject.next();
  }
  
}
