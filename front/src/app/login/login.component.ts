import {Component, OnInit} from '@angular/core';
import {ApiService} from "../http.service";
import {Router, ActivatedRoute, ParamMap} from '@angular/router';
import {UserResponse} from "../user";
import {RegisterComponent} from "../register/register.component";
import {MatDialog} from "@angular/material/dialog";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  username: string = '';
  password: string = '';
  error_text = '';
  token: any;

  constructor(private route: ActivatedRoute, private router: Router, private apiService: ApiService, public dialog: MatDialog) {
  }

  ngOnInit(): void {
  }

  login(): void {
    this.apiService.login(this.username, this.password).subscribe((data: any) => this.processLogin(data), (error: any) => this.processLoginError(error))
  }

  clear_credentials(): void {
    this.username = '';
    this.password = '';
  }

  processLogin(data: UserResponse): void {
    localStorage.setItem('token', data.token);
    localStorage.setItem('username', data.username);
    this.clear_credentials();
    this.error_text = '';
    this.router.navigate([''])
  }

  processLoginError(data: any): void {
    this.error_text = data.error.non_field_errors[0];
    this.clear_credentials();
  }

  openRegister(): void {
    let dialogRef = this.dialog.open(RegisterComponent, {
      height: '460px',
      width: '550px',
    });
  }

}
