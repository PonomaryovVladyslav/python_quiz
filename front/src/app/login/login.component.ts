import { Component, OnInit } from '@angular/core';
import {ApiService} from "../http.service";
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import {UserResponse} from "../user";

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
  constructor(private route: ActivatedRoute, private router:Router, private apiService: ApiService) {
  }

  ngOnInit(): void {
  }

  login(): void {
    this.apiService.login(this.username, this.password).subscribe((data:any) => this.processLogin(data),(error:any) => this.processLoginError(error) )
  }
  clear_credentials():void{
    this.username = '';
    this.password = '';
  }
  processLogin(data:UserResponse): void{
    localStorage.setItem('token', data.token);
    localStorage.setItem('username', data.username);
    this.clear_credentials();
    this.error_text = '';
    this.router.navigate([''])
  }
  processLoginError(data:any): void{
    this.error_text = data.error.non_field_errors[0];
    this.clear_credentials();


  }

}
