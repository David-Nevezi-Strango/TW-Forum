import { Injectable } from '@angular/core';
import { Discussion } from 'src/models/Discussion';
import { DISCUSSIONS } from 'src/mock-data/mock-discussions';
import { Observable,of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DiscussionService {

  constructor() { }

  getDiscussions(id:number):Observable<Discussion[]>{
    let result:Discussion[]=[]
    for(let d of DISCUSSIONS){
      if (d.tag_id==id){
        result.push(d)
      }
    }
    return of(result)
  }
}
