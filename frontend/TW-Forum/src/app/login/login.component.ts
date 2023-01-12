import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../services/authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private authenticationService:AuthenticationService,private _snackBar: MatSnackBar) { }

  username:string=""
  password:string=""

  ngOnInit(): void {
  }

  login(){
    this.authenticationService.login(this.username,this.password).subscribe({
      next:data=>{
        localStorage.setItem("token",data.token)
        window.location.reload()
      },
      error:error=>{
        console.log('There was an error authenticating',error)
      }
    })
  }

}
