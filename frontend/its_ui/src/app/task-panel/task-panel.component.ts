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
  task_python_code: string = '';
  code_language: string = 'python';

  task: { task_id?: string; task?: string; } = {};

  constructor(
    private client: HttpClient,
    private eventShareService: EventShareService,
    private dataShareService: DataShareService,
    ){
      this.eventSubscription = this.eventShareService.newTaskButtonClick$.subscribe(() => {
        this.fetch_task(undefined, "test_user");
      });
    }

  fetch_task(task_id?: string, user_id?: string) {
    var task_url: string;
    if (typeof task_id !== 'undefined') {
      task_url = `http://127.0.0.1:8000/task/${task_id}`;
      console.log(task_url)
    }
    else if (typeof user_id !== 'undefined') {
      task_url = `http://127.0.0.1:8000/task/for_user/${user_id}`;
      console.log(task_url);
    }
    else {
      console.log("invalid task request, aborting")
      return
    }
    this.client.get<any>(task_url, ).subscribe((data) => { this.task = {
      task_id: data.task_id,
      task: data.task
    };
    //TODO: render task as markdown using: https://www.npmjs.com/package/ngx-markdown
    this.task_python_code = this.task['task']!;
    this.dataShareService.emitTaskId(this.task.task_id!);
  });
 }


  ngOnInit(): void {
    this.fetch_task("1", undefined);
  }
}
