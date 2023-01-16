import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { AuthenticationService } from './services/authentication.service';
import { NotificationService } from './services/notification.service';
import { Notification } from 'src/models/Notification';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'TW-Forum';
  opened=false;
  authenticated=false
  notification_list:Notification[]|undefined

  constructor(public dialog: MatDialog,private authenticationService:AuthenticationService,private notificationService:NotificationService){}

  ngOnInit():void{
    let token=localStorage.getItem("token")
    if(token!=null && token!=''){
      this.authenticated=true
    }
    else{
      this.authenticated=false
    }

    let notification_id_str=localStorage.getItem("notification_id")
    //console.log(notification_id_str)
    let notification_id=parseInt(notification_id_str!)
    this.getNotifications(notification_id)
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

  getNotifications(id:number){
    this.notificationService.getNotifications(id).subscribe(response=>this.notification_list=response)
  }
}
