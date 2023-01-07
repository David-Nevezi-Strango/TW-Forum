import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  constructor() { }

  email:string=""
  username:string=""
  password:string=""

  ngOnInit(): void {
  }

  register(){
    console.log(this.email)
    console.log(this.username)
    console.log(this.password)
  }

}
