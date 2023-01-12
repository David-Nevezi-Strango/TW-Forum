import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { AuthenticationService } from './services/authentication.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'TW-Forum';
  opened=false;
  authenticated=false
  constructor(public dialog: MatDialog,private authenticationService:AuthenticationService){}

  ngOnInit():void{
    let token=localStorage.getItem("token")
    if(token!=null && token!=''){
      this.authenticated=true
    }
    else{
      this.authenticated=false
    }
  }

  openLoginDialog(): void {
    const dialogRef = this.dialog.open(LoginComponent, {
    });
  }

  openRegisterDialog(): void {
    const dialogRef = this.dialog.open(RegisterComponent, {
    });
  }

  logout(){
    this.authenticationService.logout()
  }

}
