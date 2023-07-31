import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-task-panel',
  templateUrl: './task-panel.component.html',
  styleUrls: ['./task-panel.component.css']
})
export class TaskPanelComponent {
//   task_python_code: string = `#Implementiere die Fakultät von n
// #Nutze die folgende Signatur
// def factorial(n):
//       ...`;
  task_python_code: string = '';
  code_language: string = 'python';

  task: { task_id?: string; task?: string; } = {};

  constructor(
    private client: HttpClient
    ){}

  fetch_task(task_id: string) {
    const task_url = `http://127.0.0.1:8000/task/${task_id}`
    this.client.get<any>(task_url, ).subscribe((data) => { this.task = {
      task_id: data.task_id,
      task: data.task
    };
    this.task_python_code = this.task['task']!;
  });
 }

 ngOnInit(): void {
  this.fetch_task("1");
 }
}
