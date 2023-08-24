import { Component } from '@angular/core';
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

  private eventSubscription: Subscription;
  task_markdown: string = '';
  code_language: string = 'python';

  task: { task_id?: string; task?: string; } = {};

  constructor(
    private client: HttpClient,
    private eventShareService: EventShareService,
    private dataShareService: DataShareService,
    ){
      this.eventSubscription = this.eventShareService.newTaskButtonClick$.subscribe(() => {
        this.fetch_task();
      });
    }

  fetch_task(task_unique_name?: string) {
    var task_url: string;
    if (typeof task_unique_name == 'undefined') {
      task_url = `http://127.0.0.1:8000/task/for_user`;
      console.log(task_url);
    }
    else {
      task_url = `http://127.0.0.1:8000/task/by_name/${task_unique_name}`;
      console.log(task_url);
    }
    this.client.get<any>(task_url, {withCredentials: true}).subscribe((data) => { this.task = {
      task_id: data.task_id,
      task: data.task
    };
    this.task_markdown = this.task['task']!;
    this.dataShareService.emitTaskId(this.task.task_id!);
  });
 }

  ngOnInit(): void {
    this.fetch_task();
  }
}
