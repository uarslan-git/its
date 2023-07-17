import { Component} from '@angular/core';
import { FormControl } from '@angular/forms';

// import { FormBuilder } from '@angular/forms';
// import { fromEvent, Subscription } from 'rxjs';
// import { PrismHighlightService } from './shared/services/prism-highlight.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Tutoring System for Programming';
  name = new FormControl('');

}
