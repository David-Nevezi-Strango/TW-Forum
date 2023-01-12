import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { DiscussionService } from '../services/discussion.service';
import { Discussion } from 'src/models/Discussion';
import { CommentService } from '../services/comment.service';

@Component({
  selector: 'app-discussion-detail',
  templateUrl: './discussion-detail.component.html',
  styleUrls: ['./discussion-detail.component.scss']
})
export class DiscussionDetailComponent implements OnInit {

  constructor(private route: ActivatedRoute,private location: Location,private discussionService:DiscussionService,private commentService:CommentService) { }
  discussion:Discussion|undefined
  display=false

  ngOnInit(): void {
    this.getDiscussion()
  }

  getDiscussion():void{
    const id=Number(this.route.snapshot.paramMap.get('id'));
    this.discussionService.getDiscussion(id).subscribe(discussion=>{
      this.discussion=discussion
    })
  }

  toggleAddComment(){
    this.display=!this.display
  }
}
