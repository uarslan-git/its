import { Component, Renderer2,  AfterViewChecked, AfterViewInit, ElementRef, OnDestroy, OnInit, ViewChild, EventEmitter, Output, HostListener, Input, ViewChildren, QueryList } from '@angular/core';

//Prism
import { FormBuilder } from '@angular/forms'
import { fromEvent, Subscription } from 'rxjs';
import { PrismHighlightService } from 'src/app/shared/services/prism-highlight.service'

import { DataShareService } from 'src/app/shared/services/data-share.service';
import { EventShareService } from 'src/app/shared/services/event-share.service';

@Component({
  selector: 'app-code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls: ['./code-editor.component.css']
})
export class CodeEditorComponent {
  
  @Output() codeChangeEvent : EventEmitter<string> = new EventEmitter<string>();
  timer: any; 

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

  private clearCodeChangeTimer(): void {
    clearTimeout(this.timer);
  }

// Text Area with syntax highlighting and line numbers
// At this point, the solution is not very stable.
// It relies on growing the textarea (form) and the rendered
// code synchronosly using scripts and html properties from
// different elements.
submitted_code: string = ''
code_language = 'python';

@ViewChild('textArea', { static: true })
textArea!: ElementRef;
@ViewChild('codeContent', { static: true })
codeContent!: ElementRef;
/* @ViewChild('pre', { static: true })
pre!: ElementRef; */
@ViewChild('codeContainer', { static: true })
codeContainer!: ElementRef;
@ViewChild('editorForm', {static: true})
editorForm!: ElementRef;

sub!: Subscription;
highlighted = false;
codeType = 'python';

form = this.fb.group({
  content: ''
});

get contentControl(): string {
  const content: any = this.form.get('content')?.value;
  return content != null ? content : '';
}

get userContentControl() {
  const content: any = this.form.get('content')?.value;
  if (content.startsWith(this.prefix)) {
    return content.slice(this.prefix.length);
  }
  else {
   console.error("Code prefix not present!") 
  }
}

newTaskSubscription: Subscription;
current_task_id: string = "";
prefix: string = "";

constructor(
  private prismService: PrismHighlightService,
  private fb: FormBuilder,
  private renderer: Renderer2,
  private dataShareService: DataShareService,
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
      this.form.setValue({'content': ''});
  });
}


ngOnInit(): void {
  this.listenForm()
  // This subscription runs code every time the user changes the code.
  //TODO: onTextareaKeydown does the same in principal. Check if this should be handled in same method.
  this.form.controls.content.valueChanges.subscribe((newValue) => {
    if(this.prefix.length <= 0) {
      this.prefix = sessionStorage.getItem("taskPrefix")!;  
    }
    newValue = this.ensurePrefix(newValue!);
    this.synchronizedTextareaGrow();
    this.clearCodeChangeTimer();
    this.emitCodeChangeEventTimer(newValue!);
  });
}

ngAfterViewInit() {
  this.prismService.highlightAll();
}

ngAfterViewChecked() {
  if (this.highlighted) {
    this.prismService.highlightAll();
    this.highlighted = false;
  }
}

ngOnDestroy() {
  this.sub?.unsubscribe();
}

private ensurePrefix(newContent: string){
  const prefix = sessionStorage.getItem("taskPrefix")!
  if(!(newContent.startsWith(prefix))) {
    console.log("Ensuring prefix");
    newContent = prefix + newContent.slice(prefix.length);
    this.form.setValue({'content': newContent});
  }
  return(newContent);
}

private synchronizedTextareaGrow() {
  // subtract padding
  const minHeight = this.codeContainer.nativeElement.offsetHeight - 15;
  const minWidth = this.codeContainer.nativeElement.offsetWidth - 70;

  const toHeight = Math.max(this.editorForm.nativeElement.offsetHeight, minHeight);
  // Add Padding (70px) and font size (16px)
  const toWidth = Math.max(this.codeContent.nativeElement.offsetWidth + 70 + 16, minWidth);
  this.renderer.setProperty(this.textArea.nativeElement, 'style', `height: ${toHeight}px;width: ${toWidth}px;overflow:hidden;`)
  this.renderer.setProperty(this.editorForm.nativeElement, 'style', `width: ${toWidth}px;overflow:hidden;`)
}

private listenForm() {
  this.sub = this.form.valueChanges.subscribe((val) => {
    // const modifiedContent = this.prismService.convertHtmlIntoString(val.content!);
    this.renderer.setProperty(this.codeContent.nativeElement, 'innerHTML', val.content!);
    this.highlighted = true;
  });
}

onTextareaKeyDown(event: KeyboardEvent): void {
  if (event.key === 'Tab') {
    event.preventDefault(); // Prevent the default tab behavior
    const start = this.textArea.nativeElement.selectionStart;
    const end = this.textArea.nativeElement.selectionEnd;
  
    // Get the current content of the textarea
    const currentContent = this.contentControl;

    // Insert four spaces at the current cursor position
    const newContent = currentContent.substring(0, start) + '    ' + currentContent.substring(end);

    this.form.setValue({'content': newContent});

    // Move the cursor to the end of the inserted spaces
    const newCursorPosition = start + 4;
    this.textArea.nativeElement.setSelectionRange(newCursorPosition, newCursorPosition);
  }
}

onSelect(event: Event) {
  const start = this.textArea.nativeElement.selectionStart;
  const end = this.textArea.nativeElement.selectionEnd;
  if (start == end) {
    if (start <= this.prefix.length) {
      this.textArea.nativeElement.setSelectionRange(this.prefix.length, this.prefix.length);
    }
  }
}
}
