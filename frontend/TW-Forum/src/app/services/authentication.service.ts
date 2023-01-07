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

  login(data:Object):Observable<Object>{
    return this.http.post<Object>(this.login_url,data)
  }
}
