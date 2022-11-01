import { Injectable } from '@angular/core';
import { Tag } from 'src/tag';
import { TAGS } from 'src/mock-tags';

@Injectable({
  providedIn: 'root'
})
export class TagService {

  constructor() { }

  getTags():Tag[]{
    return TAGS;
  }
}
