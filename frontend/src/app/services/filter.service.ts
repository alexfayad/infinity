import { Injectable } from '@angular/core';
import {Subject} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FilterService {
  public filterSource = new Subject<any>();
  filter = this.filterSource.asObservable();
  constructor() { }

  changeFilter(selected_filter: any) {
    this.filterSource.next(selected_filter);
  }
}


