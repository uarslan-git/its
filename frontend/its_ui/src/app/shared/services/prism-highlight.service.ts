import { Injectable } from '@angular/core';

// Prism as service tutorial
// Tutorial: https://www.youtube.com/watch?v=avByjLNGV3E

import 'prismjs';
import 'prismjs/plugins/line-numbers/prism-line-numbers';
import 'prismjs/components/prism-css';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-markup';
import 'prismjs/components/prism-typescript';
import 'prismjs/components/prism-sass';
import 'prismjs/components/prism-scss';
import 'prismjs/components/prism-python';

declare var Prism: any;

@Injectable({
  providedIn: 'root',
})
export class PrismHighlightService {
  constructor() {}
  
  highlightAll() {
    Prism.highlightAll();
  }

  // TODO: Remove unecessary HTML stuff
/*   convertHtmlIntoString(text: string) {
    return text
      .replace(new RegExp('&', 'g'), '&amp;')
      .replace(new RegExp('<', 'g'), '&lt;');
  } */
}