import { Component, Renderer2,  AfterViewChecked, AfterViewInit, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';

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

  submitted_code: string = ''
  code_language = 'python';

// Text Area with syntax highlighting and line numbers
// At this point, the solution is not very stable.
// It relies on growing the textarea (form) and the rendered 
// code synchronosly using scripts and html properties from
// different elements. 

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
  this.newTaskSubscription = this.eventShareService.newTaskEvent$.subscribe(
    () => {
      console.log("Editor Content reset!");     
/*       this.textArea.nativeElement.content = '';
           this.codeContent.nativeElement.content = '';
           this.editorForm.nativeElement.content = ''; */
           this.form.setValue({'content': ''});
          }
  );

}

ngOnInit(): void {
  this.listenForm()
  /* this.synchronizeScroll(); */
  this.form.controls.content.valueChanges.subscribe((newValue) => {
    this.synchronizedTextareaGrow();
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
  console.log(toWidth)
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

/* private synchronizeScroll() {
  const localSub  = fromEvent(this.textArea.nativeElement, 'scroll').subscribe(() => {
    const toTop = this.textArea.nativeElement.scrollTop;
    const toLeft = this.textArea.nativeElement.scrollLeft;

    this.renderer.setProperty(this.pre.nativeElement, 'scrollTop', toTop);
    this.renderer.setProperty(this.pre.nativeElement, 'scrollLeft', toLeft + 0.2);
  });

  this.sub.add(localSub);
} */

}
