import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {LoginComponent} from "./login/login.component";
import {QuestionnaireComponent} from "./questionnaire/questionnaire.component";
import {UnapprovedUsersComponent} from "./unapproved-users/unapproved-users.component";

const routes: Routes = [
  {path: '', component: QuestionnaireComponent},
  {path: 'login', component: LoginComponent},
  {path: 'unapproved', component: UnapprovedUsersComponent},
  {path: '**', redirectTo: ''},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
