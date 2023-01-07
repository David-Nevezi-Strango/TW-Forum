import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../services/authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private authenticationService:AuthenticationService) { }

  email:string=""
  password:string=""

  ngOnInit(): void {
  }

  login(){
    let data={"email":this.email,"password":this.password}
    this.authenticationService.login(data).subscribe(response=>{console.log(response)})
  }

}
