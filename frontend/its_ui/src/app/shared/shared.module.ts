import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
/* import { PrismComponent } from './components/prism/prism.component'; */
import { MarkdownModule } from 'ngx-markdown';

// Add prism languages (for prism.component)
// TODO: Maybe refactor to be inside sub-module/sub-component?
/* import 'prismjs/plugins/line-numbers/prism-line-numbers'
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-java'; */
import { MarkdownPanelComponent } from './components/markdown-panel/markdown-panel.component';


@NgModule({
  declarations: [/* PrismComponent,  */MarkdownPanelComponent],
  imports: [
    CommonModule,
    MarkdownModule.forChild(),
    // ReactiveFormsModule
  ],
  exports: [/* PrismComponent,  */MarkdownPanelComponent]
})
export class SharedModule {}
