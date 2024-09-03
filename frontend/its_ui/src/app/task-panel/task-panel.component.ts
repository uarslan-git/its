import { Component, ElementRef, ViewChild, Input, AfterViewInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { EventShareService } from '../shared/services/event-share.service';
import { Subscription, delay } from 'rxjs';
import { environment } from 'src/environments/environment';
import { CourseSettingsService } from '../shared/services/course-settings-service.service';

import { MarkdownPanelComponent } from '../shared/components/markdown-panel/markdown-panel.component';

@Component({
  selector: 'app-task-panel',
  templateUrl: './task-panel.component.html',
  styleUrls: ['./task-panel.component.css']
})
export class TaskPanelComponent {

  @ViewChild("courseCompleteDialog", {static: true}) courseCompleteDialog!: ElementRef<HTMLDialogElement>;
  @ViewChild(MarkdownPanelComponent) markdownPanelComponent!: MarkdownPanelComponent;
  @Input() initTask?: string | null = null;

  private eventSubscription: Subscription;
  task_markdown: string = '';
  code_language: string = 'python';

  //@Input() course: {unique_name?: string; curriculum?: string[]} = {}
  course: {unique_name?: string; curriculum?: string[]} = {}
  task: {unique_name?: string; task?: string; type?: string, prefix?: string, 
    arguments?: string[], possible_choices?: string, feedback_available?: string} = {};

  constructor(
    private client: HttpClient,
    private eventShareService: EventShareService,
    private courseSettingsService: CourseSettingsService
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
        task: data.task,
        type: data.type,
        prefix: data.prefix,
        arguments: data.arguments,
        possible_choices: data.possible_choices,
        feedback_available: data.feedback_available,
    };
    console.log("new task request")
    if (this.task['unique_name'] == "course completed") {
      delay(100);
      this.courseCompleteDialog.nativeElement.showModal();
    }
    this.task_markdown = this.task['task']!;
    //console.log(this.task['unique_name'])
    //this.dataShareService.emitTaskId(this.task['unique_name']!);
    
    sessionStorage.setItem("taskId", this.task['unique_name']!);
    sessionStorage.setItem("taskType", this.task['type']!);
    sessionStorage.setItem("taskArguments", JSON.stringify(this.task['arguments']!));
    sessionStorage.setItem("taskPrefix", this.task['prefix']!);
    sessionStorage.setItem("taskChoices", JSON.stringify(this.task['possible_choices']!));
    sessionStorage.setItem("feedbackAvailable", this.task["feedback_available"]!);
    this.markdownPanelComponent.resetScroll();
    this.eventShareService.emitNewTaskFetchedEvent();

  });
 }

/*   ngOnInit(): void {
    // Fetch the first task with timeout in order to load the whole app.
    setTimeout(()=>{  
      const courseID = sessionStorage.getItem("courseID")
      this.client.get<any>(`${environment.apiUrl}/course/get/${courseID}`, {withCredentials: true}).subscribe(
        (data) => {
          this.course = {
            unique_name: data.unique_name,
            curriculum: data.curriculum,
          }
        }
      ); 
      console.log(this.initTask);                        
      if (this.initTask == null) {
        this.fetch_task();
      }
      else {
        this.fetch_task(this.initTask);
      }
  }, 300);
  } */

  ngAfterViewInit(){
    this.courseSettingsService.getCourse().subscribe((course) =>
    {
      this.course = course
      if (this.initTask == null) {
        this.fetch_task();
      }
      else {
        this.fetch_task(this.initTask);
      }
    });

  }

  ngOnDestroy() {
    this.eventSubscription.unsubscribe();
  }

}
