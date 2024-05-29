import { Component, OnInit, OnDestroy, AfterViewInit, ElementRef, ViewChild } from '@angular/core';
import { MonacoEditorService } from '../../services/monaco-edito-service.service';
import { first } from 'rxjs';

declare var monaco: any;

@Component({
  selector: 'app-monaco-code-editor',
  templateUrl: './monaco-code-editor.component.html',
  styleUrls: ['./monaco-code-editor.component.css']
})
export class MonacoCodeEditorComponent implements AfterViewInit {

  constructor(private monacoEditorService: MonacoEditorService){
    monacoEditorService.load();
  }

  public _editor: any;
  @ViewChild('editorContainer', { static: true })_editorContainer!: ElementRef;

  private initMonaco(): void {
    if(!this.monacoEditorService.loaded) {
      this.monacoEditorService.loadingFinished.pipe(first()).subscribe(() => {
        this.initMonaco();
      });
      return;
    }

    this._editor = monaco.editor.create(
      this._editorContainer.nativeElement,
      {"theme": "vs-dark"}
    );
  }

  ngAfterViewInit(): void {
    this.initMonaco();
  }
}
