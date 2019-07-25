import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { API_URL } from 'src/app/constants/urls';
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(private http: HttpClient) { }
  tokenHeader() {
    const headers = new HttpHeaders({'Authorization': 'Token ' + localStorage.getItem('token')});
        return { headers: headers };
}
  public auth_check(login_details) {

   const options = this.tokenHeader();
   try {
     return this.http.post(API_URL + 'get_token/', login_details);
   } catch (e) {
     console.log(e);
   }

  }
}
