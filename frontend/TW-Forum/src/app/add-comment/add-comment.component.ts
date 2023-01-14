import { ThisReceiver } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { Output, EventEmitter } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommentService } from '../services/comment.service';

@Component({
  selector: 'app-add-comment',
  templateUrl: './add-comment.component.html',
  styleUrls: ['./add-comment.component.scss']
})
export class AddCommentComponent implements OnInit {

  constructor(private route: ActivatedRoute,private commentService:CommentService) { }

  @Output() closed = new EventEmitter<string>();
  comment:string=""

  ngOnInit(): void {
  }

  close(){
    this.comment=""
    this.closed.emit('closed')
  }

  submit(){
    const id=Number(this.route.snapshot.paramMap.get('id'));
    let date = new Date().toLocaleDateString()
    let data={"date":date,"text":this.comment}
    this.commentService.addComment(id,data).subscribe()
  }
}
