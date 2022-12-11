import { Injectable } from '@angular/core';
import { Tag } from 'src/models/tag';
import { TAGS } from 'src/mock-data/mock-tags';

@Injectable({
  providedIn: 'root'
})
export class TagService {

  constructor() { }

  getTags():Tag[]{
    return TAGS;
  }
}
