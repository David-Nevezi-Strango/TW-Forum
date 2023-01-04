import { Component, OnInit } from '@angular/core';
import { TagService } from '../services/tag.service';
import { Tag } from 'src/models/tag';
import { TAGS } from 'src/mock-data/mock-tags';

@Component({
  selector: 'app-tag',
  templateUrl: './tag.component.html',
  styleUrls: ['./tag.component.scss']
})
export class TagComponent implements OnInit {

  constructor(private tagService:TagService) { }

  tags:Tag[]=[]
  selected!:Tag

  ngOnInit(): void {
    this.getTags();
  }

  getTags(){
    this.tagService.getTags().subscribe(tags=>{this.tags=tags}); 
  }

}
