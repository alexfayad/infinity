import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { login_url } from 'src/app/constants/urls';
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(private http: HttpClient) { }
  tokenHeader() {
    const headers = new HttpHeaders({'Authorization': 'Token ' + localStorage.getItem('token')});
        return { headers: headers };
}
  public login(login_details) {
     return this.http.post(login_url + 'get_token/', login_details);
  }
  public signup(signup_details) {
     return this.http.post(login_url + 'signup/', signup_details);
  }
  public check_login() {
    const token = localStorage.getItem('token');
      if (token) {
      return true;
    }
      return false;
  }
}
