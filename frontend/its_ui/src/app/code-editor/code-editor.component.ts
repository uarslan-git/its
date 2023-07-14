import { Component, Renderer2 } from '@angular/core';

//Prism
import { FormBuilder } from '@angular/forms'
import { FormControl } from '@angular/forms';
import { Subscription } from 'rxjs'; // Notwendig?
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

  sub!: Subscription;
  highlighted = false;
  codeType = 'html';

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


}
