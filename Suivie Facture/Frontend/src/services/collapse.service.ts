import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CollapseService {
  private isCollapsedSubject = new BehaviorSubject<boolean>(false);
  isCollapsed$ = this.isCollapsedSubject.asObservable();

  constructor() { }

  toggleCollapse() {
    this.isCollapsedSubject.next(!this.isCollapsedSubject.value);
  }
}
