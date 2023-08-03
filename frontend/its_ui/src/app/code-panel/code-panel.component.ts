import { Component, Renderer2,  AfterViewChecked, AfterViewInit, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';

//Prism
import { FormBuilder } from '@angular/forms'
import { fromEvent, Subscription } from 'rxjs';
import { PrismHighlightService } from '../shared/services/prism-highlight.service'
import { HttpClient } from '@angular/common/http';

import { DataShareService } from '../shared/services/data-share.service';

@Component({
  selector: 'app-code-panel',
  templateUrl: './code-panel.component.html',
  styleUrls: ['./code-panel.component.css'],
})
export class CodePanelComponent {

  submitted_code: string = ''
  code_language = 'python';

  //Submit Button
  submitButtonClicked() {
    this.submitted_code = this.contentControl;
    this.client.post<any>('http://127.0.0.1:8000/code_submit', {task_id: this.current_task_id, code: this.submitted_code, log: "True"}).subscribe(data => {
      console.log(data["test_results"]);
    console.log(this.submitted_code)
    });
  }

  // Text Area with syntax highlighting and line numbers
  @ViewChild('textArea', { static: true })
  textArea!: ElementRef;
  @ViewChild('codeContent', { static: true })
  codeContent!: ElementRef;
  @ViewChild('pre', { static: true })
  pre!: ElementRef;

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

  taskIdSubscription: Subscription;
  current_task_id: string = "";

  constructor(
    private prismService: PrismHighlightService,
    private fb: FormBuilder,
    private renderer: Renderer2,
    //!!!!!!
    private client: HttpClient,
    private dataShareService: DataShareService,
  ) {
    this.taskIdSubscription = this.dataShareService.taskIdShare$.subscribe(
      (data) => (this.current_task_id = data)
    );
  }

  ngOnInit(): void {
    this.listenForm()
    this.synchronizeScroll();
    //!!!!!!
    this.client.get<any>('http://127.0.0.1:8000/status').subscribe((data) =>  {
      console.log(data["message"]);
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

  private listenForm() {
    this.sub = this.form.valueChanges.subscribe((val) => {
      const modifiedContent = this.prismService.convertHtmlIntoString(val.content!);

      // TODO: Remove uneccesary HTML stuff
      this.renderer.setProperty(this.codeContent.nativeElement, 'innerHTML', modifiedContent);

      this.highlighted = true;
    });
  }

  private synchronizeScroll() {
    const localSub  = fromEvent(this.textArea.nativeElement, 'scroll').subscribe(() => {
      const toTop = this.textArea.nativeElement.scrollTop;
      const toLeft = this.textArea.nativeElement.scrollLeft;

      this.renderer.setProperty(this.pre.nativeElement, 'scrollTop', toTop);
      this.renderer.setProperty(this.pre.nativeElement, 'scrollLeft', toLeft + 0.2);
    });

    this.sub.add(localSub);
  }
}
