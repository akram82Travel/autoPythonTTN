import { OfService } from '../../services/of.service';
import { Component, OnInit } from '@angular/core';
import { CollapseService } from '../../services/collapse.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-of',
  templateUrl: './of.component.html',
  styleUrls: ['./of.component.css']
})
export class OfComponent implements OnInit {
  ofs: any[] = [];
  selectedOf: string | null = null;
  df_num: string = '';
  RefMarche: string = '';

  constructor(
    private router: Router,
    public collapseService: CollapseService,
    private ofService: OfService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.df_num = params['df_num'];
      this.RefMarche = params['RefMarche'];
      if (this.df_num) {
        this.fetchOfs();
      } else {
        console.error('df_num is missing from queryParams');
      }
    });
  }

  async fetchOfs(): Promise<void> {
    if (this.df_num && this.df_num.length > 0) {
      try {
        const data = await this.ofService.getOfs(this.df_num, this.RefMarche);
        this.ofs = data.OFS || [];
      } catch (error) {
        console.error('Error fetching OFs:', error);
      }
    }
  }

  toggleMenu(): void {
    this.collapseService.toggleCollapse();
  }

  navigateToTicket(of: any): void {
    this.selectedOf = of;
    console.log('Navigating to Ticket with OFD_Lot:', of.OFD_Lot);
    this.router.navigate(['/ticket'], { queryParams: { OF_num: of.OFD_Lot} });
  }
}
