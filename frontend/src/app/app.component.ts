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
  video_modal = false;
  login_modal = false;
  LoginForm = new FormGroup({
  confirm_email : new FormControl('', [Validators.required, Validators.email]),
  username: new FormControl('', Validators.required),
  password: new FormControl('', Validators.required),
  });
    constructor(
    private apiService: ApiService,
    private activatedRoute: ActivatedRoute,
    private currencyService: CurrencyService,
    private authservice: AuthService,
     ) {
    this.currentCurrency = this.currencyService.current;
  }

  ngOnInit() {
    this.apiService.getShops().subscribe((shops: Shop[]) => this.shops = shops);
    this.activatedRoute.queryParams.pipe().subscribe(params => {
      this.products = [];
      this.apiService.getFilteredProducts(<ProductParams>{...params})
        .pipe(
          tap((response: ProductResponse) => this.nextPage = response.next),
          map((response: ProductResponse) => response.results),
        ).subscribe(products => this.products = products);
    });
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
  onSubmit() {
      console.log('submit');
      const username = this.LoginForm.value['username'];
      const password = this.LoginForm.value['password'];
      const login_details = {'username' : username, 'password' : password};

      this.authservice.auth_check(login_details).subscribe(data => {
        if (data['token']) {
          localStorage.setItem('token', data['token']);
          this.video_modal = true;
          this.login_modal = false;
          } else {
          console.log('something went wrong');
        }
      });
  }
}
