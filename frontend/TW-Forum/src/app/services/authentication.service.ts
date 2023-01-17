import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable,of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  constructor(private http: HttpClient) { }
  register_url="http://localhost:5000/signup"
  login_url="http://localhost:5000/login"

  register(data:Object):Observable<Object>{
    return this.http.post<Object>(this.register_url,data)
  }

  login(username:string,password:string):Observable<any>{
    let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'Authorization': 'Basic ' + btoa(username + ':' + password)
      })
    };

    let data={"username":username,"password":password}
    return this.http.post<Object>(this.login_url,data,httpOptions)
  }

  logout(){
    localStorage.setItem("token",'')
    localStorage.setItem("user_id",'')
    localStorage.setItem("notification_id",'')
    window.location.reload()
  }
}
