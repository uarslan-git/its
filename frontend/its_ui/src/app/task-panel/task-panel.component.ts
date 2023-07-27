import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-task-panel',
  templateUrl: './task-panel.component.html',
  styleUrls: ['./task-panel.component.css']
})
export class TaskPanelComponent {
  task_python_code: string = `#Implementiere die Fakultät von n
#Nutze die folgende Signatur
def factorial(n):
      ...`;
  code_language: string = 'python'
}
