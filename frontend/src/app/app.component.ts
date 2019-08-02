import {Component, OnInit} from '@angular/core';
import {faInfinity} from '@fortawesome/free-solid-svg-icons';
import {map, tap} from 'rxjs/operators';
import {ProductParams, ProductResponse} from './interfaces/common';
import {ApiService} from './services/api.service';
import {AuthService} from './services/auth.service';
import {ActivatedRoute} from '@angular/router';
import {Product} from './interfaces/product';
import {Shop} from './interfaces/shop';
import {Currency, currencyItems} from 'src/app/constants/currency';
import {Observable} from 'rxjs';
import {CurrencyService} from 'src/app/services/currency.service';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { environment } from 'src/environments/environment';
import {Output} from '@angular/core';
import {EventEmitter} from '@angular/core';
import {FilterService} from './services/filter.service';
import {Router} from '@angular/router';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  assets_url = environment.assets_url;
  faCoffee = faInfinity;
  nextPage: string;
  products: Product[] = [];
  shops: Shop[] = [];
  menuItems = [
    {name: 'Shops'},
    {name: 'FAQ'}
  ];
  activeMenuItem = '';
  currency = [...currencyItems];
  currentCurrency: Observable<Currency>;
  shopname: any;
  video_modal = false;
  login_modal = false;
  signup_modal = false;
  login_error = '';
  signup_error = ''
  login_status: boolean;
  wishlist_count = 0;
  LoginForm = new FormGroup({
  confirm_email : new FormControl('', [Validators.required, Validators.email]),
  username: new FormControl('', Validators.required),
  password: new FormControl('', Validators.required),
  });
  SignupForm = new FormGroup({
  email : new FormControl('', [Validators.required, Validators.email]),
  name: new FormControl('', Validators.required),
  username: new FormControl('', Validators.required),
  password: new FormControl('', Validators.required),
  confirm_password: new FormControl('', Validators.required),
  });
    constructor(
    private apiService: ApiService,
    private activatedRoute: ActivatedRoute,
    private currencyService: CurrencyService,
    private authservice: AuthService,
    private filterservice: FilterService,
    private router: Router,
     ) {
    this.currentCurrency = this.currencyService.current;
  }

  ngOnInit() {
    this.apiService.getShops().subscribe((shops: Shop[]) => this.shops = shops);
    this.filterservice.filter.subscribe(message => this.shopname = message);
    this.login_status = this.authservice.check_login();
    this.activatedRoute.queryParams.pipe().subscribe(params => {
      this.products = [];
      this.apiService.getFilteredProducts(<ProductParams>{...params})
        .pipe(
          tap((response: ProductResponse) => this.nextPage = response.next),
          map((response: ProductResponse) => response.results),
        ).subscribe(products => this.products = products);
    });
    if (this.login_status === true) {
         this.apiService.getWishlist().subscribe(data => {
           // @ts-ignore
           this.wishlist_count = data.length;
           this.apiService.wishlists.subscribe(message => this.wishlist_count = message);
         });
    }
  }

  openMenuForItem(menuItem: string) {
    if (this.activeMenuItem === menuItem) {
      this.activeMenuItem = '';
    } else {
      this.activeMenuItem = menuItem;
    }
  }

  changeCurrency(currency): void {
    this.currencyService.setCurrentCurrency(currency.code);
  }
  changeFilter(selected_filter): void {
      if (this.shopname) {
        this.router.navigate(['/'], { queryParams: { shop_name: this.shopname, link__sex: selected_filter } });
      } else {
        this.router.navigate(['/'], { queryParams: { link__sex: selected_filter } });
      }
  }
  onLogin() {
      const username = this.LoginForm.value['username'];
      const password = this.LoginForm.value['password'];
      const login_details = {'username' : username, 'password' : password};

      this.authservice.login(login_details).subscribe(data => {
        if (data['token']) {
          localStorage.setItem('token', data['token']);
          this.login_status = true;
          this.video_modal = true;
          this.login_modal = false;
          } else {
          console.log('something went wrong');
        }
      }, error => {
           if (error) {
                this.login_error = 'Please enter correct username and password';
           }
        });
  }
  onSignup() {
      const name = this.SignupForm.value['name'];
      const username = this.SignupForm.value['username'];
      const email = this.SignupForm.value['email'];
      const password = this.SignupForm.value['password'];
      const confirm_password = this.SignupForm.value['confirm_password'];
      const signup_details = {'username': username, 'first_name': name, 'email': email, 'password': password};
      console.log(password, confirm_password)
      if ( password.length >= 8 && password === confirm_password) {
        this.authservice.signup(signup_details).subscribe(data => {
          if (data['sucess']) {
            this.signup_modal = false;
            this.login_modal = true;
          }
          else {
            this.signup_error = 'Username already exists';
          }
      });
    }
  }
  logout() {
      localStorage.removeItem('token');
      this.login_status = false;
  }
}
