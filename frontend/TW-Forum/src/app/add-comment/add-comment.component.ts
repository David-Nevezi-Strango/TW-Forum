import { Component, OnInit } from '@angular/core';
import { Output, EventEmitter } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { COMMENTS } from 'src/mock-data/mock-comments';

@Component({
  selector: 'app-add-comment',
  templateUrl: './add-comment.component.html',
  styleUrls: ['./add-comment.component.scss']
})
export class AddCommentComponent implements OnInit {

  constructor(private route: ActivatedRoute) { }

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
  }
}
