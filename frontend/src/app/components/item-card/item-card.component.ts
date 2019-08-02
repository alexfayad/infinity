import { Component, Input, OnInit } from '@angular/core';
import { Product } from '../../interfaces/product';
import { environment } from 'src/environments/environment';
import { Currency } from 'src/app/constants/currency';
import {ApiService} from '../../services/api.service';


@Component({
  selector: 'app-item-card',
  templateUrl: './item-card.component.html',
  styleUrls: ['./item-card.component.scss']
})
export class ItemCardComponent implements OnInit {
  assets_url = environment.assets_url;
  @Input() item: Product;
  @Input() currency: Currency;
  @Input() coefficient: number;

  constructor(private api: ApiService) {}

  ngOnInit() {

  }

  public routeToProductURL() {
    window.open(`${environment.vigLink}?u=${encodeURIComponent(this.item.url_original)}&key=${environment.vigKey}`);
  }
  addTowishlist(product_id) {
    this.api.addWishlist({'productid': product_id}).subscribe(data => {
      // @ts-ignore
      this.api.wishlist_source.next(data.length);
  });
  }
}
