import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { reglementFatService } from '../../services/reglementFat.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ColDef, RowStyle,GridOptions  } from 'ag-grid-community';

// Define the interface for the data structure returned from the API
export interface Reglement {
  Doc_Num: string;
  Reg_Num: string;
  RegD_Montant: number;
  RegD_Devise_Cours: number;
  Devise_Code: string;
  isTotalRow: boolean;
}

@Component({
  selector: 'app-liste-reglement',
  templateUrl: './liste-reglement.component.html',
  styleUrls: ['./liste-reglement.component.css']
})
export class ListeReglementComponent implements OnInit {
  public grandTotalRow: "top" | "bottom" = "bottom";
  displayedColumns: string[] = ['Doc_Num', 'Reg_Num', 'RegD_Montant', 'RegD_Devise_Cours', 'Devise_Code' ];
  pageSizeOptions: number[] = [13, 20, 50, 100, 150, 200];
  dataSource: any[] = [];
  dataSourcefact: any[] = [];
  Fact_num: string = '';
  PaimentFact: any[] = [];
  selectedMethod: string = '';
  rowDataWithTotal: any[] = [];
  facture: any;
  totalMontant: number = 0;
  totalDeviseCours: number = 0;

  columnDefs: ColDef[] = [
    { field: 'Doc_Num', sortable: true, filter: true },
    { field: 'Reg_Num', sortable: true, filter: true },
    { field: 'RegD_Montant', sortable: true, filter: true },
    { field: 'RegD_Devise_Cours', sortable: true, filter: true },
    { field: 'Devise_Code', sortable: true, filter: true }
  ];
  
  gridOptions: GridOptions = { groupIncludeFooter: true, groupIncludeTotalFooter: true };
  public rowData: Reglement[] = [];

  constructor(
    public dialogRef: MatDialogRef<ListeReglementComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private fb: FormBuilder,
    private reglementFatService: reglementFatService,
    private route: ActivatedRoute
  ) {
    this.facture = data.facture;
    this.Fact_num = data.facture.Facture;
    this.fetchModeRegFact();
  }

  ngOnInit(): void {
  }
  totalFooterRow: any = {};
  calculateTotals() {
    const totalMontant = parseFloat(this.rowData.reduce((sum, row) => sum + row.RegD_Montant, 0).toFixed(3));
    const totalDeviseCours = parseFloat(this.rowData.reduce((sum, row) => sum + row.RegD_Devise_Cours, 0).toFixed(4));
    
    this.totalFooterRow = {
      Doc_Num: 'Total',
      Reg_Num: '',
      RegD_Montant: totalMontant,
      RegD_Devise_Cours: totalDeviseCours,
      Devise_Code: '',
    };
    this.rowData = [...this.rowData, this.totalFooterRow];
  }
 
  async fetchModeRegFact(): Promise<void> {
    if (this.Fact_num) {
      try {
        const data = await this.reglementFatService.getregFact(this.Fact_num);
        this.PaimentFact = data.ModePaiement || [];
        this.rowData = data.ModePaiement || [];
        this.calculateTotals(); // Recalculate totals after data fetch
      } catch (error) {
        console.error('Error fetching Liste Reglement for Fact_num:', error);
      }
    }
  }

  onNoClick(): void {
    this.dialogRef.close();
  }
  getRowStyle = (params: any) => {
    // Style the total row differently
    if (params.data.isTotalRow) {
      return { fontWeight: 'bold', backgroundColor: '#f0f0f0' };
    }
    return null;
  };
}
