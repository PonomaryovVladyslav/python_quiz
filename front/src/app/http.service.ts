import {Injectable} from '@angular/core';

import {HttpClient, HttpParams, HttpHeaders} from '@angular/common/http';
import {Observable, throwError} from 'rxjs';
import {map, catchError} from 'rxjs/operators';


@Injectable({providedIn: 'root'})
export class ApiService {

  baseURL: string = "http://localhost:8000/api/";

  constructor(private http: HttpClient) {
  }

  //Any Data Type
  login(username: string, password: string): Observable<any> {
    return this.http.post(this.baseURL + 'login/', {'username': username, "password": password})
  }
}
