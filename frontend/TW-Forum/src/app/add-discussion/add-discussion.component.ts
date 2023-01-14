import { Component, OnInit } from '@angular/core';
import { DiscussionService } from '../services/discussion.service';

@Component({
  selector: 'app-add-discussion',
  templateUrl: './add-discussion.component.html',
  styleUrls: ['./add-discussion.component.scss']
})
export class AddDiscussionComponent implements OnInit {

  constructor(private discussionService:DiscussionService) { }

  title:string=""
  tag:string=""
  description:string=""

  ngOnInit(): void {
  }

  addDiscussion(){
    let discussion={"title":this.title,"tag_name":this.tag,"description":this.description}
    this.discussionService.addDiscussion(discussion).subscribe(response=>window.location.reload())
    //window.location.reload()
  }

}
