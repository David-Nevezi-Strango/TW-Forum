import { Injectable } from '@angular/core';
import { Observable,of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Notification } from 'src/models/Notification';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  constructor(private http: HttpClient) { }
  url="http://localhost:5000/notifications"

  getNotifications(id:number):Observable<Notification[]>{
    let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'x-access-tokens': 'Bearer ' + localStorage.getItem("token")
      })
    };
    return this.http.get<Notification[]>(`${this.url}/${id}`,httpOptions)
  }

  updateNotification(id:number):Observable<Object>{
    let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'x-access-tokens': 'Bearer ' + localStorage.getItem("token")
      })
    };
    return this.http.post<Object>(`${this.url}/${id}`,id,httpOptions)
  }
}
