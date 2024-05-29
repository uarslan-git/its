import { Component, Output, EventEmitter, ElementRef, ViewChild, OnInit, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-code-editor-new',
  templateUrl: './code-editor-new.component.html',
  styleUrls: ['./code-editor-new.component.css']
})
export class CodeEditorNewComponent {

  @Output() codeChangeEvent : EventEmitter<string> = new EventEmitter<string>();

}
