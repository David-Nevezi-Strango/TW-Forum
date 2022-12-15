import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Comment } from 'src/models/Comment';
import { COMMENTS } from 'src/mock-data/mock-comments';

@Injectable({
  providedIn: 'root'
})
export class CommentService {

  constructor() { }

  getComments(id:number):Observable<Comment[]>{
    let result:Comment[]=[]
    for(let comment of COMMENTS){
      if(comment.discussion_id==id){
        result.push(comment);
      }
    }
    return of(result)
  }
}
