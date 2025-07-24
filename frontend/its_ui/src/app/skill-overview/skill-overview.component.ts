import { Component, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { EventEmitter } from '@angular/core';

export interface CourseDescription{
  unique_name: string;
  display_name: string;
}
@Component({
  selector: 'app-skill-overview',
  templateUrl: './skill-overview.component.html',
  styleUrls: ['./skill-overview.component.css']
})
export class SkillOverviewComponent {

  @ViewChild('reasonPopup', {static: true}) reasonPopup!: ElementRef<HTMLDialogElement>;
  @ViewChild('explanationPopup', {static: true}) explanationPopup!: ElementRef<HTMLDialogElement>;

  reasonMarkdown: string = '';
  explanationMarkdown: string = '';

  courses : CourseDescription[]= [];
  selectedCourse : string | null = null;

  course_value  = 59;
  course_progress = 15; 

  skills : any[] = []
  
  constructor(
      private client: HttpClient,
    ){
    }

  ngOnInit(): void {
    this.fetchCourseInfo()
  }

  //TODO: only do this for courses the user is enrolled in (needs additional request)
  fetchCourseInfo(){
    const endpoint_url = `${environment.apiUrl}/course/info/`;
    this.client.get<any>(endpoint_url, {withCredentials: true}).subscribe((data) => { 
      this.courses =  data.course_list;
      if (this.courses.length > 0)
      {
        this.selectedCourse = this.courses[0].unique_name
        this.loadSkillsForCourse(this.courses[0].unique_name)
      }
  });
  }

  onSelectedCourseChange() {
    var e : any = document.getElementById("skill-overview-course-selection")
    var newValue = e.value
    this.selectedCourse = newValue
    console.log(`Selected option: ${this.selectedCourse}`);

    this.loadSkillsForCourse(newValue)
  }

  loadSkillsForCourse(courseUniqueName: string){
    const endpoint_url = `${environment.apiUrl}/skills/${courseUniqueName}/`;
    this.client.get<any>(endpoint_url, {withCredentials: true}).subscribe((data) => {
      this.skills = data.skill_list
    })
  }
  

  generateExplanation(skillName: string){
    this.explanationMarkdown = "# Explanation\nHere is an explanation for skill " + skillName;
    this.explanationPopup.nativeElement.showModal();
  }

  generateReason(skillName: string){
    this.reasonMarkdown = "# Reason\nHere is a reason for skill " + skillName;
    this.reasonPopup.nativeElement.showModal();
  }

}
