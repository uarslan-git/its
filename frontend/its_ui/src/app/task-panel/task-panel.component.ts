import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { EventShareService } from '../shared/services/event-share.service';
import { DataShareService } from '../shared/services/data-share.service';
import { Subscription, delay } from 'rxjs';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-task-panel',
  templateUrl: './task-panel.component.html',
  styleUrls: ['./task-panel.component.css']
})
export class TaskPanelComponent {

  @ViewChild("courseCompleteDialog", {static: true}) courseCompleteDialog!: ElementRef<HTMLDialogElement>

  private eventSubscription: Subscription;
  task_markdown: string = '';
  code_language: string = 'python';

  course: {unique_name?: string; curriculum?: string[]} = {}
  task: { unique_name?: string; task?: string; } = {};

  constructor(
    private client: HttpClient,
    private eventShareService: EventShareService,
    private dataShareService: DataShareService,
    ){
      this.eventSubscription = this.eventShareService.newTaskEvent$.subscribe((message) => {
        this.selectAndFetchTask(message);
      });
    }

  selectAndFetchTask(message: string) {
    console.log(message)
    const curriculum = this.course.curriculum!;
    const current_task_name = this.task.unique_name!;
    const task_index: number = curriculum.findIndex((element) => element == current_task_name);
    if (message == 'next') {
      //TODO: Think about whether to allow clicking through next tasks.
      if (task_index == (curriculum.length-1)) {
        alert("No further task availiable")
        return;
      }
      console.log(curriculum[task_index+1])
      this.fetch_task(curriculum[task_index+1]);
    }
    if (message == 'previous') {
      if (task_index == 0) {
        alert("Previous Task doesn't exist");
        return;
      }
      this.fetch_task(curriculum[task_index-1]);
    }
    if (message == 'personal') {
      this.fetch_task();
    }
  }

  fetch_task(task_unique_name?: string) {
    var task_url: string;
    if (typeof task_unique_name == 'undefined') {
      task_url = `${environment.apiUrl}/task/for_user`;
    }
    else {
      task_url = `${environment.apiUrl}/task/by_name/${task_unique_name}`;
    }
    this.client.get<any>(task_url, {withCredentials: true}).subscribe(
      (data) => { 
      this.task = {
        unique_name: data.unique_name,
        task: data.task
    };
    console.log("new task request")
    if (this.task['unique_name'] == "course completed") {
      delay(100);
      this.courseCompleteDialog.nativeElement.showModal();
    }
    this.task_markdown = this.task['task']!;
    //console.log(this.task['unique_name'])
    this.dataShareService.emitTaskId(this.task['unique_name']!);
  });
 }

  ngOnInit(): void {
    this.fetch_task();
    this.client.get<any>(`${environment.apiUrl}/course/get`, {withCredentials: true}).subscribe(
      (data) => {
        this.course = {
          unique_name: data.unique_name,
          curriculum: data.curriculum,
        }
        console.log(this.course);
      }
    );
  }
}
