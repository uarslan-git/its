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
  selectedCourse : CourseDescription | null = null;

  course_value  = 59;
  course_progress = 15; 
  
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
        this.selectedCourse = this.courses[0]
      }
  });
  }

  skills1 : any[] =[
    {
      name: "skill1",
      value : 50,
      progress : 25,
      explanation : "This is a nice LLM-generated explanation",
      associated_tasks: ["task1", "task2", "task5"]
    },
    {
      name: "skill2",
      value : 75,
      progress : 20,
      explanation : "This is a nice LLM-generated explanation",
      associated_tasks: ["task2", "task5"]
    },
    {
      name: "skill3",
      value : 30,
      progress : 10,
      explanation : "This is a nice LLM-generated explanation",
      associated_tasks: ["task1", "task5"]
    }
  ]

  skills = this.skills1

  skills2 : any[] =[
    {
      name: "skill1",
      value : 50,
      progress : 25,
      explanation : "This is a nice LLM-generated explanation",
      associated_tasks: ["task1", "task2", "task5"]
    },
    {
      name: "skill2",
      value : 75,
      progress : 20,
      explanation : "This is a nice LLM-generated explanation",
      associated_tasks: ["task2", "task5"]
    }
  ]

  onSelectedCourseChange(event: Event) {
    var newValue = "course2"
    this.selectedCourse = {unique_name:"course2", display_name: "Course2"};
    console.log(`Selected option: ${this.selectedCourse}`);

    if(newValue == "course2"){
      this.skills = this.skills2
    }
    else{
      this.skills = this.skills1
    }
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
