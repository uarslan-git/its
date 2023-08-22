import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-markdown-panel',
  templateUrl: './markdown-panel.component.html',
  styleUrls: ['./markdown-panel.component.css']
})
export class MarkdownPanelComponent {
  @Input() markdownString: string="";
}