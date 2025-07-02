import { Component } from '@angular/core';
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


  courses : CourseDescription[]= [];
  selectedCourse : CourseDescription | null = null;
  
  constructor(
      private client: HttpClient,
    ){
    }

  ngOnInit(): void {
    this.fetchCourseInfo()
  }

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
    window.alert(`Explanation for skill with name ${skillName}`)
  }

  generateReason(skillName: string){
    window.alert(`Reason for skill with name ${skillName}`)
  }

}
