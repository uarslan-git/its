import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MarkdownModule } from 'ngx-markdown';
import { MarkdownPanelComponent } from './components/markdown-panel/markdown-panel.component';
import { DataTermsPopupComponent } from './components/data-terms-popup/data-terms-popup.component';


@NgModule({
  declarations: [MarkdownPanelComponent, DataTermsPopupComponent],
  imports: [
    CommonModule,
    MarkdownModule.forChild(),
    // ReactiveFormsModule
  ],
  exports: [MarkdownPanelComponent, DataTermsPopupComponent]
})
export class SharedModule {}
