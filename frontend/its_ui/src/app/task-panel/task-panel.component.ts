import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { EventShareService } from '../shared/services/event-share.service';
import { DataShareService } from '../shared/services/data-share.service';
import { Subscription } from 'rxjs';

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

  task: { unique_name?: string; task?: string; } = {};

  constructor(
    private client: HttpClient,
    private eventShareService: EventShareService,
    private dataShareService: DataShareService,
    ){
      this.eventSubscription = this.eventShareService.newTaskEvent$.subscribe(() => {
        this.fetch_task();
      });
    }

  fetch_task(task_unique_name?: string) {
    var task_url: string;
    if (typeof task_unique_name == 'undefined') {
      task_url = `http://127.0.0.1:8000/task/for_user`;
    }
    else {
      task_url = `http://127.0.0.1:8000/task/by_name/${task_unique_name}`;
    }
    this.client.get<any>(task_url, {withCredentials: true}).subscribe((data) => { this.task = {
      unique_name: data.unique_name,
      task: data.task
    };
    console.log("new task request")
    if (this.task['unique_name'] == "course completed") {
      //alert("Awesome, you have completed the course! There are no tasks left to solve :)");
      this.courseCompleteDialog.nativeElement.showModal();
      return;
    }
    this.task_markdown = this.task['task']!;
    //console.log(this.task['unique_name'])
    this.dataShareService.emitTaskId(this.task['unique_name']!);
  });
 }

  ngOnInit(): void {
    this.fetch_task();
  }
}
