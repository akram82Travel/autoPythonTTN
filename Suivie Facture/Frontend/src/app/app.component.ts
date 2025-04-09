import { BreakpointObserver } from '@angular/cdk/layout';
import { CollapseService } from '../services/collapse.service';
import {
  Component,
  ViewChild,
} from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  title = 'material-responsive-sidenav';
  @ViewChild(MatSidenav)
  sidenav!: MatSidenav;
  isMobile= true;
  isCollapsed = true;

  constructor(private observer: BreakpointObserver,public collapseService: CollapseService) {}

  ngOnInit() {
    this.observer.observe(['(max-width: 800px)']).subscribe((screenSize) => {
      if(screenSize.matches){
        this.isMobile = true;
      } else {
        this.isMobile = false;
      }
    });
  }
   toggleMenu() {
  if (this.isMobile) {
    this.sidenav.toggle();
    this.collapseService.toggleCollapse(); // Toggle collapse state
  } else {
    this.sidenav.open();
    this.isCollapsed = !this.isCollapsed;
    this.collapseService.toggleCollapse(); // Toggle collapse state
  }
}

}
