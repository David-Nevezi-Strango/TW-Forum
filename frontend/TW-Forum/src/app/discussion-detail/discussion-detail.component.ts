import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { DiscussionService } from '../services/discussion.service';
import { Discussion } from 'src/models/Discussion';
import { CommentService } from '../services/comment.service';
import {MatDialog, MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import { LoginComponent } from '../login/login.component';

@Component({
  selector: 'app-discussion-detail',
  templateUrl: './discussion-detail.component.html',
  styleUrls: ['./discussion-detail.component.scss']
})
export class DiscussionDetailComponent implements OnInit {

  constructor(private route: ActivatedRoute,private location: Location,private discussionService:DiscussionService,private commentService:CommentService,public dialog: MatDialog) { }
  discussion:Discussion|undefined
  display=false
  belongs_to_current_user=false
  user_id:number|undefined

  ngOnInit(): void {
    this.getDiscussion()
    this.getUserID()
  }

  getUserID(){
    let user_id_str=localStorage.getItem("user_id")
    let user_id:number|undefined
    if(user_id_str!=null){
      user_id=parseInt(user_id_str)
      this.user_id=user_id
    }
  }

  getDiscussion():void{
    const id=Number(this.route.snapshot.paramMap.get('id'));
    this.discussionService.getDiscussion(id).subscribe(discussion=>{
      this.discussion=discussion
      this.belongs()
    })
  }

  deleteDiscussion(){
    this.discussionService.deleteDiscussion(this.discussion?.discussion_id!).subscribe(response=>console.log(response))
  }

  deleteComment(id:number){
    this.commentService.deleteComment(id).subscribe(response=>{
      window.location.reload()
    })
  }

  toggleAddComment(){
    let token=localStorage.getItem("token")
    if(token!=null && token!=''){
      this.display=!this.display
    }
    else{
      const dialogRef = this.dialog.open(LoginComponent, {
      
      });
    }
  }

  belongs(){
    let user_id_str=localStorage.getItem("user_id")
    let user_id:number|undefined
    if(user_id_str!=null){
      user_id=parseInt(user_id_str)
    }
    else{return}
    if(user_id==this.discussion?.user_id){
      this.belongs_to_current_user=true
    }
    else{
      this.belongs_to_current_user=false
    }
  }
}
