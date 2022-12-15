import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DiscussionDetailComponent } from './discussion-detail/discussion-detail.component';
import { DiscussionComponent } from './discussion/discussion.component';
import { HomeComponent } from './home/home.component';

const routes: Routes = [
  {path:"discussions/:id",component:DiscussionComponent},
  {path:"home",component:HomeComponent},
  {path:"discussion/:id",component:DiscussionDetailComponent},
  { path: '', redirectTo: '/home', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
