import { Component, OnInit } from '@angular/core';
import { TagService } from '../services/tag.service';
import { Tag } from 'src/models/tag';
import {MatDialog, MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import { AddDiscussionComponent } from '../add-discussion/add-discussion.component';
import { LoginComponent } from '../login/login.component';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-tag',
  templateUrl: './tag.component.html',
  styleUrls: ['./tag.component.scss']
})
export class TagComponent implements OnInit {

  constructor(private tagService:TagService,public dialog: MatDialog,private snackbar:MatSnackBar) { }

  tags:Tag[]=[]
  selected!:Tag

  ngOnInit(): void {
    this.getTags();
  }

  getTags(){
    this.tagService.getTags().subscribe(tags=>{this.tags=tags}); 
  }

  openDialog(){
    let token=localStorage.getItem("token")
    if(token!=null && token!=''){
      const dialogRef = this.dialog.open(AddDiscussionComponent, {
        
      });
    }
    else{
      const dialogRef = this.dialog.open(LoginComponent, {
      
      });
      this.snackbar.open('Trebuie să fiți autentificat pentru a pune o întrebare!', '', {
        duration: 3000
      });
    }
  }
}
