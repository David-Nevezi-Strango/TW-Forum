import { Component, OnInit } from '@angular/core';
import { TagService } from '../services/tag.service';
import { Tag } from 'src/tag';

@Component({
  selector: 'app-tag',
  templateUrl: './tag.component.html',
  styleUrls: ['./tag.component.scss']
})
export class TagComponent implements OnInit {

  constructor(private tagService:TagService) { }

  tags:Tag[]=[]

  ngOnInit(): void {
    this.getTags();
  }

  getTags(){
    this.tags=this.tagService.getTags(); 
  }

}
