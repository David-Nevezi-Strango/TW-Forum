import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../services/authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private authenticationService:AuthenticationService,private snackbar: MatSnackBar) { }

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
        this.snackbar.open('Numele de utilizator sau parola sunt incorecte!', '', {
          duration: 3000
        });
      }
    })
  }

}
