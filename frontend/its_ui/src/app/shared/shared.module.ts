import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PrismComponent } from './components/prism/prism.component';

// Add prism languages
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-java';

@NgModule({
  declarations: [PrismComponent],
  imports: [
    CommonModule
  ],
  exports: [PrismComponent]
})
export class SharedModule {}
