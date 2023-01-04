import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Comment } from 'src/models/Comment';
import { COMMENTS } from 'src/mock-data/mock-comments';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CommentService {

  constructor(private http: HttpClient) { }
  url="http://localhost:5000/discussion"

  getComments(id:number):Observable<Comment[]>{
    return this.http.get<Comment[]>(`${this.url}/${id}`)
  }
}
