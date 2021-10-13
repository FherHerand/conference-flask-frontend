import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  url: string = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) { }

  login(email: string, password: string): Observable<any> {
    let data = {
        email: email,
        password: password
      }
    return this.http.post(`${this.url}/login`, data);
  }
}