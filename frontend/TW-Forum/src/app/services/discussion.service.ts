import { Injectable } from '@angular/core';
import { Discussion } from 'src/models/Discussion';
//import { DISCUSSIONS } from 'src/mock-data/mock-discussions';
import { Observable,of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DiscussionService {

  constructor(private http: HttpClient) { }
  url="http://localhost:5000/discussions"
  single_url="http://localhost:5000/discussion"

  getDiscussions(id:number):Observable<Discussion[]>{
    return this.http.get<Discussion[]>(`${this.url}/${id}`)
  }

  getDiscussion(id:number):Observable<Discussion>{
    return this.http.get<Discussion>(`${this.single_url}/${id}`)
  }
}
