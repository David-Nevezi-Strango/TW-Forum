import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../services/authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  constructor(private authenticationService:AuthenticationService,private snackbar:MatSnackBar) { }

  email:string=""
  username:string=""
  name:string=""
  password:string=""

  ngOnInit(): void {
  }

  register(){
    let data={"email":this.email,"username":this.username,"name":this.name,"password":this.password}
    this.authenticationService.register(data).subscribe()
    this.authenticationService.login(this.username,this.password).subscribe({
      next:data=>{
        localStorage.setItem("token",data.token)
        window.location.reload()
      },
      error:error=>{
        this.snackbar.open('Un cont cu acea adresă de e-mail există deja.', '', {
          duration: 3000
        });
      }
    })

  }

}
