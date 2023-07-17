import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PrismComponent } from './components/prism/prism.component';

// Add prism languages (for prism.component)
// TODO: Maybe refactor to be inside sub-module/sub-component?
import 'prismjs/plugins/line-numbers/prism-line-numbers'
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-java';


@NgModule({
  declarations: [PrismComponent],
  imports: [
    CommonModule,
    // ReactiveFormsModule
  ],
  exports: [PrismComponent]
})
export class SharedModule {}
