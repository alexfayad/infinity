import { Component, Input } from '@angular/core';
import { Shop } from '../../interfaces/shop';
import {Router} from '@angular/router';
import {FilterService} from '../../services/filter.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-shop-list',
  templateUrl: './shop-list.component.html',
  styleUrls: ['./shop-list.component.scss']
})
export class ShopListComponent {
  @Input() shops: Shop[];
  @Input() gender: 'M' | 'W';
  assets_url = environment.assets_url;
  constructor(private router: Router, private filterservice: FilterService) {
  }
  shopfilter(shopname): void {
      this.filterservice.changeFilter(shopname);
      this.router.navigate(['/'], { queryParams: { shop_name: shopname } });
  }
  genderfilter(): void {
      this.filterservice.change_gender_Filter();
  }
}
