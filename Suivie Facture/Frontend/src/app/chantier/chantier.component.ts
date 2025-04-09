import { Component, OnInit } from '@angular/core';
import { CollapseService } from '../../services/collapse.service';
import { Router } from '@angular/router';
import { ChantierService } from '../../services/chantier.service';

@Component({
  selector: 'app-chantier',
  templateUrl: './chantier.component.html',
  styleUrls: ['./chantier.component.css']
})
export class ChantierComponent implements OnInit {
  chantiers: any[] = [];
  selectedChantier: any | null = null;

  constructor(
    private router: Router,
    public collapseService: CollapseService,
    private chantierService: ChantierService
  ) {}

  ngOnInit(): void {
    this.chantierService.getChantiers().subscribe(
      (data: any) => {
        this.chantiers = data.chantiers || [];
      },
      (error) => {
        console.error('Error fetching chantiers:', error);
      }
    );
  }

  toggleMenu() {
    this.collapseService.toggleCollapse();
  }

  navigateToOF(chantier: any) {
    this.selectedChantier = chantier;
    console.log('Navigating to OF with df_num:', chantier.DF);
    this.router.navigate(['/of'], { queryParams: { df_num: chantier.DF, RefMarche: chantier.RefMarche } });
  }
}
