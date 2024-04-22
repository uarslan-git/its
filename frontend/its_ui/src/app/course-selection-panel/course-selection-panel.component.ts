import { Component, Output, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-course-selection-panel',
  templateUrl: './course-selection-panel.component.html',
  styleUrls: ['./course-selection-panel.component.css']
})
export class CourseSelectionPanelComponent {

  @Output() courseSelected: EventEmitter<string> = new EventEmitter<string>;

  courses: string[] =  ["Lorem ipsum dolor sit amet", "Consectetur adipiscing elit"]

  constructor(
    private client: HttpClient,
    ){}

  selectCourse(courseID: string){
    this.courseSelected.emit("courseSelected")
  }

  ngOnInit(): void {
    this.fetchCourseInfo()
  }

  fetchCourseInfo(){
    const endpoint_url = `${environment.apiUrl}/course/get-course-info/`;
    this.client.get<any>(endpoint_url, ).subscribe((data) => { 
      this.courses =  data.courses
  });
  }
}
