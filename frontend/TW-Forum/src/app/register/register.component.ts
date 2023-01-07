import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../services/authentication.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  constructor(private authenticationService:AuthenticationService) { }

  email:string=""
  username:string=""
  name:string=""
  password:string=""

  ngOnInit(): void {
  }

  register(){
    let data={"email":this.email,"username":this.username,"name":this.name,"password":this.password}
    console.log(data)
    this.authenticationService.register(data).subscribe(response=>{console.log(response)})
  }

}
