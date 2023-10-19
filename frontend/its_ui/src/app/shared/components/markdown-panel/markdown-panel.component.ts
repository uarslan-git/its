import { Component, Input, ViewChild, ElementRef } from '@angular/core';

@Component({
  selector: 'app-markdown-panel',
  templateUrl: './markdown-panel.component.html',
  styleUrls: ['./markdown-panel.component.css']
})
export class MarkdownPanelComponent {
  @Input() markdownString: string="";
  @ViewChild("markdownContainer", {static: true}) markdownContainer!: ElementRef;



  resetScroll(){
    this.markdownContainer.nativeElement.scrollTop = 0;
  }
}