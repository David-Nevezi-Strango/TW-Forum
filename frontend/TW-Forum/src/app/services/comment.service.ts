import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Comment } from 'src/models/Comment';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CommentService {

  constructor(private http: HttpClient) { }
  url="http://localhost:5000/discussion"
  comment_url="http://localhost:5000"

  getComments(id:number):Observable<Comment[]>{
    return this.http.get<Comment[]>(`${this.url}/${id}`)
  }

  addComment(id:number,comment:Object): Observable<Comment> {
    let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'x-access-tokens': 'Bearer ' + localStorage.getItem("token")
      })
    };
    return this.http.post<Comment>(`${this.url}/${id}`, comment,httpOptions)
  }

  deleteComment(id:number){
    let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'x-access-tokens': 'Bearer ' + localStorage.getItem("token")
      })
    };
    return this.http.delete<void>(`${this.comment_url}/${id}`)
  }
}
