import { Component, Output, EventEmitter, ElementRef, ViewChild } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { EventShareService } from 'src/app/shared/services/event-share.service';

@Component({
  selector: 'app-action-panel',
  templateUrl: './action-panel.component.html',
  styleUrls: ['./action-panel.component.css']
})
export class ActionPanelComponent {

  @Output() runEvent: EventEmitter<string> = new EventEmitter<any>();
  @Output() submitEvent : EventEmitter<string> = new EventEmitter<string>();

  @ViewChild("runDialog", {static: true}) runDialog!: ElementRef<HTMLDialogElement>

  submissionId: string = '';

  runParametersForm!: FormGroup;

  constructor(private eventShareService: EventShareService,
              private fb: FormBuilder){}

  ngOnInit() {
/*      this.runParametersForm = this.fb.group({
      fields: this.fb.array(this.parameterFormArrayControls())
    }); */
  }

  parameterFormArrayControls() {
    const controls: FormGroup[] = [];

    const argArray: string[] = JSON.parse(sessionStorage.getItem("taskArguments")!);
    if (!argArray) {
      console.error("taskArguments is not present in sessionStorage.");
    }
    for (let i = 0; i < argArray.length; i++) {
      controls.push(this.fb.group({
        // You can add any validators or default values here
        argname: argArray[i],
        textField: [''],
      }));
    }
    return controls;
  }

  get runFormArrayControls() {
    return (this.runParametersForm.get('fields') as FormArray).controls;
  }

  //run Button
  runButtonClicked() {
    if(sessionStorage.getItem("taskType") == "function") {
      this.runParametersForm = this.fb.group({
        fields: this.fb.array(this.parameterFormArrayControls())
      });
      this.runDialog.nativeElement.showModal();
    }
    else {
      this.emitRunEvent({});
    }
  }

  sendWithParameters() {
    var parameters: any = {};
    const count = JSON.parse(sessionStorage.getItem("taskArguments")!).length;
    for (let i = 0; i < count; i++) {
      const control = this.runFormArrayControls.at(i)!;
      const key = control.get('argname')!.value;
      const value = control.get('textField')!.value;
      parameters[key] = value;
    }
    this.runDialog.nativeElement.close();
    this.emitRunEvent(parameters);
  }

  emitRunEvent(parameters: any) {
    this.runEvent.emit(parameters);
    this.eventShareService.emitRunButtonClick();
  }

  //Submit Button
  submitButtonClicked() {
    this.submitEvent.emit();
    this.eventShareService.emitSubmitButtonClick();
  }
}
