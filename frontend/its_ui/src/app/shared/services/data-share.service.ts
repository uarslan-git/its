import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataShareService {

  constructor() { }

  //Task Id share
  private taskIdShareSubject = new Subject<string>();

  taskIdShare$ = this.taskIdShareSubject.asObservable();

  emitTaskId(task_id: string) {
    this.taskIdShareSubject.next(task_id);
  }
}

