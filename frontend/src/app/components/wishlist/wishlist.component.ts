import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../services/api.service';
import {Product} from '../../interfaces/product';
import {ProductParams, ProductResponse} from '../../interfaces/common';
import {map, tap} from 'rxjs/operators';
import {environment} from "../../../environments/environment";



@Component({
  selector: 'app-wishlist',
  templateUrl: './wishlist.component.html',
  styleUrls: ['./wishlist.component.scss']
})
export class WishlistComponent implements OnInit {
  nextPage: string;
  wishlist:  any;
  constructor(private apiService: ApiService) { }

  ngOnInit() {
     this.apiService.getWishlist(
        ).subscribe(products => this.wishlist = products);
  }
  public routeToProductURL(original_url) {
    window.open(`${environment.vigLink}?u=${encodeURIComponent(original_url)}&key=${environment.vigKey}`);
  }
}
