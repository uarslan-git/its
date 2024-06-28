import { Component, Output, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

export interface CourseDescription{
  unique_name: string;
  display_name: string;
}
@Component({
  selector: 'app-course-selection-panel',
  templateUrl: './course-selection-panel.component.html',
  styleUrls: ['./course-selection-panel.component.css']
})
export class CourseSelectionPanelComponent {

  @Output() courseSelected: EventEmitter<string> = new EventEmitter<string>;

  courses: CourseDescription[] = [];

  course_names: string[] =  [];

  constructor(
    private client: HttpClient,
    ){}

  selectCourse(courseID: string){
    sessionStorage.setItem("courseID", courseID);
    const endpoint_url = `${environment.apiUrl}/course/select`;
    const body = {
      'course_unique_name': courseID};
    this.client.post(endpoint_url, body, {withCredentials: true}).subscribe();
    this.courseSelected.emit("courseSelected");
  }

  ngOnInit(): void {
    this.fetchCourseInfo()
  }

  fetchCourseInfo(){
    const endpoint_url = `${environment.apiUrl}/course/info/`;
    this.client.get<any>(endpoint_url, {withCredentials: true}).subscribe((data) => { 
      this.courses =  data.course_list;
  });
  }
}
