import { Injectable } from '@angular/core';
import {Subject} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FilterService {
  public filterSource = new Subject<any>();
  filter = this.filterSource.asObservable();
  public genderfilterSource = new Subject<any>();
  gender_filter = this.filterSource.asObservable();

  constructor() { }

  changeFilter(selected_filter: any) {
    this.filterSource.next(selected_filter);
  }
  change_gender_Filter() {
    this.genderfilterSource.next(true);
  }
}


