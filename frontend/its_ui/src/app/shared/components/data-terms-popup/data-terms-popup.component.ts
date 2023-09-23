import { Component, ViewChild, ElementRef, Input,  } from '@angular/core';

@Component({
  selector: 'app-data-terms-popup',
  templateUrl: './data-terms-popup.component.html',
  styleUrls: ['./data-terms-popup.component.css']
})
export class DataTermsPopupComponent {

  @ViewChild("dataTermsPopup", {static: true}) dataTermsPopup!: ElementRef<HTMLDialogElement>


  showPopup() {
      this.dataTermsPopup.nativeElement.showModal();
    }
}
