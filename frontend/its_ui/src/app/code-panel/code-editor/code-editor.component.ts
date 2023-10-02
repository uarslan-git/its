import { Component, Renderer2,  AfterViewChecked, AfterViewInit, ElementRef, OnDestroy, OnInit, ViewChild, EventEmitter, Output, HostListener } from '@angular/core';

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
        this.codeChangeEvent.emit(newVal);
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

newTaskSubscription: Subscription;
current_task_id: string = "";

constructor(
  private prismService: PrismHighlightService,
  private fb: FormBuilder,
  private renderer: Renderer2,
  private dataShareService: DataShareService,
  private eventShareService: EventShareService,
) {
  this.newTaskSubscription = this.eventShareService.newTaskFetched$.subscribe(
    () => {
            console.log("Editor Content reset!");
            // store current program state, if a new task is selected
            this.codeChangeEvent.emit(this.contentControl);
            this.form.setValue({'content': ''});
          }
  );
}

ngOnInit(): void {
  this.listenForm()
  // This subscription runs code every time the user changes the code.
  //TODO: onTextareaKeydown does the same in principal. Check if this should be handled in same method.
  this.form.controls.content.valueChanges.subscribe((newValue) => {
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
/*     const modifiedContent = this.prismService.convertHtmlIntoString(val.content!); */
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
}

