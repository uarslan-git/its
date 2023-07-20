import { Component, Renderer2,  AfterViewChecked, AfterViewInit, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';

//Prism
import { FormBuilder } from '@angular/forms'
import { fromEvent, Subscription } from 'rxjs'; // Notwendig?
import { PrismHighlightService } from '../shared/services/prism-highlight.service'

//!!!!!!! Für Requests
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls: ['./code-editor.component.css'],
})
export class CodeEditorComponent {

  task_python_code: string = `#Implementiere die Fakultät von n
#Nutze die folgende Signatur
def factorial(n):
      ...`;
  submitted_code: string = ''
  code_language = 'python';

  //Submit Button
  submitButtonClicked() {
    this.submitted_code = this.contentControl;
    this.client.post<any>('http://127.0.0.1:8000/code_submit', {task_id: 1, code: this.submitted_code}).subscribe(data => {
      console.log(data["test_results"])
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

  constructor(
    private prismService: PrismHighlightService,
    private fb: FormBuilder,
    private renderer: Renderer2,
    //!!!!!!
    private client: HttpClient
  ) {}

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
