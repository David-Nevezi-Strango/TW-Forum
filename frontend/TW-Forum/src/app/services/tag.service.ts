import { Injectable } from '@angular/core';
import { Tag } from 'src/models/tag';
import { TAGS } from 'src/mock-data/mock-tags';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TagService {

  constructor(private http: HttpClient) { }
  url="localhost:5000/tags"

  getTags():Observable<Tag[]>{
    return this.http.get<Tag[]>(this.url)
  }

  /*
  getTags():Observable<Tag[]>{
    return of(TAGS)
  }
  */

  getTag(id:number):Observable<Tag>{
    for(let tag of TAGS){
      if(tag.tag_id==id){
        return of(tag)
      }
    }
    return of(TAGS[0])
  }
}
