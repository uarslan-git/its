import { Component, Renderer2,  AfterViewChecked, AfterViewInit, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';

//Prism
import { FormBuilder } from '@angular/forms'
import { FormControl } from '@angular/forms';
import { fromEvent, Subscription } from 'rxjs'; // Notwendig?
import { PrismHighlightService } from '../shared/services/prism-highlight.service'

@Component({
  selector: 'app-code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls: ['./code-editor.component.css']
})
export class CodeEditorComponent {

  // content = new FormControl('');

  python_code = 'print("Hello World")';
  code_language = 'python';

  // // Dynamik syntax highlighting
  // sub! : Subscription;
  // highlighted = false;
  // codeType = 'python';

  // text = 'print("Hallo")';


  // get contentControl() {
  //   return this.form.get('content');
  // }

  // sub!: Subscription;
  // highlighted = false;
  // codeType = 'html';

  // form = this.fb.group({
  //   content: ''
  // });

  // get contentControl() {
  //   return this.form.get('content');
  // }

  // constructor(
  //   private prismService: PrismHighlightService,
  //   private fb: FormBuilder,
  //   private renderer: Renderer2
  // ) {}

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

  get contentControl() {
    return this.form.get('content');
  }

  constructor(
    private prismService: PrismHighlightService,
    private fb: FormBuilder,
    private renderer: Renderer2
  ) {}

  ngOnInit(): void {
    this.listenForm()
    this.synchronizeScroll();
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
