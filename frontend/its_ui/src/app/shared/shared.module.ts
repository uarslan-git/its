import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PrismComponent } from './components/prism/prism.component';

// Add prism languages

import 'prismjs/plugins/line-numbers/prism-line-numbers'
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-java';

// Prism as service tutorial
// Tutorial: https://www.youtube.com/watch?v=avByjLNGV3E
import { ReactiveFormsModule } from '@angular/forms';
import { PrismHighlightService } from './services/prism-highlight.service'

@NgModule({
  declarations: [PrismComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  exports: [PrismComponent]
})
export class SharedModule {}
