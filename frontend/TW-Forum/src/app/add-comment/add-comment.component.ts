import { Component, OnInit } from '@angular/core';
import { Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-add-comment',
  templateUrl: './add-comment.component.html',
  styleUrls: ['./add-comment.component.scss']
})
export class AddCommentComponent implements OnInit {

  constructor() { }

  @Output() closed = new EventEmitter<string>();
  comment:string=""

  ngOnInit(): void {
  }

  close(){
    this.comment=""
    this.closed.emit('closed')
  }

  submit(){
    console.log(this.comment)
  }
}
