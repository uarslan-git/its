import { Component, EventEmitter, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormGroup, FormControl} from '@angular/forms';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-course-settings',
  templateUrl: './course-settings.component.html',
  styleUrls: ['./course-settings.component.css']
})
export class CourseSettingsComponent {

  @Output() settingsClosedEvent: EventEmitter<string> = new EventEmitter<string>

  settingsForm!: FormGroup;

  course: any;
  course_settings_list: any;

  constructor(private client: HttpClient){
    this.settingsForm = new FormGroup({
      feedback_init_time: new FormControl(0),
      feedback_cooldown: new FormControl(0),
    });
  }

  ngOnInit(){

    const course_id = sessionStorage.getItem("courseID");
    this.client.get<any>(`${environment.apiUrl}/course/get_settings/${course_id}`, {"withCredentials": true}).subscribe(
      (data) => {
        this.course = {
          unique_name: data.unique_name,
          curriculum: data.curriculum,
        };
        this.course_settings_list = data.course_settings_list;
        this.settingsForm.patchValue({
          feedback_init_time: +this.course_settings_list[0].feedback_init_time,
          feedback_cooldown: +this.course_settings_list[0].feedback_cooldown,
        });
      }
    );
  }

  saveSettings(): void {
    const course_id = sessionStorage.getItem("courseID");
    var data = this.settingsForm.value
    data.course_id = course_id
    this.client.post<any>(`${environment.apiUrl}/course/update_settings`, data, {"withCredentials": true}).subscribe()
  }

  closeSettings(): void {
    this.settingsClosedEvent.emit("settingsClosed")
  }
}
