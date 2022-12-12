import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { DiscussionService } from '../services/discussion.service';
import { Discussion } from 'src/models/Discussion';

@Component({
  selector: 'app-discussion',
  templateUrl: './discussion.component.html',
  styleUrls: ['./discussion.component.scss']
})
export class DiscussionComponent implements OnInit {

  constructor(private route: ActivatedRoute,private location: Location,private discussionService:DiscussionService) { }
  tag_id:number|undefined;
  discussions:Discussion[]=[]

  ngOnInit(): void {
    this.getDiscussions()
  }

  getDiscussions():void{
    const id=Number(this.route.snapshot.paramMap.get('id'));
    this.discussionService.getDiscussions(id).subscribe(discussions=>{
      this.discussions=discussions;
      console.log(this.discussions)
    })
  }

}
