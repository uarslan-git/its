import { Component, Output, EventEmitter, ElementRef, ViewChild, OnInit, AfterViewInit} from '@angular/core';
import { Subscription } from 'rxjs';
import { MonacoCodeEditorComponent } from 'src/app/shared/components/monaco-code-editor/monaco-code-editor.component';
import { EventShareService } from 'src/app/shared/services/event-share.service';

@Component({
  selector: 'app-code-editor-new',
  templateUrl: './code-editor-new.component.html',
  styleUrls: ['./code-editor-new.component.css']
})
export class CodeEditorNewComponent {

  @Output() codeChangeEvent : EventEmitter<string> = new EventEmitter<string>();
  language: string = "python";

  @ViewChild(MonacoCodeEditorComponent) monacoCodeEditorComponent!: MonacoCodeEditorComponent;

  timer: any; 


  newTaskSubscription: Subscription;
  current_task_id: string = "";
  prefix: string = "";

  constructor(
    private eventShareService: EventShareService,
  ) {
    this.newTaskSubscription = this.eventShareService.newTaskFetched$.subscribe(() => {
        //TODO: Better control time of execution, because codePanel is also listening to newTaskFetched!
        if (typeof this.prefix !== 'undefined') {
          this.prefix = sessionStorage.getItem('taskPrefix')!;
        }
        else {
          this.codeChangeEvent.emit(this.userContentControl);
          this.prefix = sessionStorage.getItem('taskPrefix')!;
        }
    });
  }

  // Provide editor content
  get contentControl(): string {
    //const content: any = this.form.get('content')?.value;
    const content: any = this.monacoCodeEditorComponent.getContent();
    return content != null ? content : '';
  }
  
  get userContentControl() {
    const content: any = this.monacoCodeEditorComponent.getContent();
    if (content.startsWith(this.prefix)) {
      return content.slice(this.prefix.length);
    }
    else {
     console.error("Code prefix not present!") 
    }
  }

  //Set Editor Content
  setEditorContent(value: string) {
    this. monacoCodeEditorComponent.setContent(value);
  }

  onEditorContentChange(event: Event){
    const newContent = this.contentControl;
    clearTimeout(this.timer);
    this.emitCodeChangeEventTimer(newContent);
    this.ensurePrefix(newContent);
  }

  private ensurePrefix(newContent: string){
    const prefix = sessionStorage.getItem("taskPrefix")!
    if(!(newContent.startsWith(prefix))) {
      console.log("Ensuring prefix");
      newContent = prefix + newContent.slice(prefix.length + 1);
      this.setEditorContent(newContent);
    }
    return(newContent);
  }

  // The Timer is set every time the user code changes, if it changes again,
  // the timer is reset
  emitCodeChangeEventTimer(newVal: string) {
    this.timer = setTimeout(
      () => {
        const prefix = sessionStorage.getItem('taskPrefix')!;
        if (newVal.startsWith(prefix)) {
          this.codeChangeEvent.emit(newVal.slice(prefix.length));
        }
      }
    , 1000) //Milliseconds timeout
  }

  ngOnDestroy() {
    this.newTaskSubscription.unsubscribe();
  }

}
