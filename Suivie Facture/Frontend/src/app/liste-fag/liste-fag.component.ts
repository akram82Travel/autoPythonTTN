import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { listeFagService } from '../../services/listeFag.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ColDef, RowStyle,GridOptions  } from 'ag-grid-community';

// Define the interface for the data structure returned from the API
export interface Reglement {
  Doc_Num: string;
  Doc_RS: string;
  Doc_Date: Date;
  Doc_TTTC: number;
  isTotalRow: boolean;
}

@Component({
  selector: 'app-liste-fag',
  templateUrl: './liste-fag.component.html',
  styleUrl: './liste-fag.component.css'
})
export class ListeFagComponent implements OnInit {
  public grandTotalRow: "top" | "bottom" = "bottom";
  displayedColumns: string[] = ['Doc_Num', 'Doc_RS', 'Doc_Date', 'Doc_TTTC' ];
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
    { headerName:'N° Facture',field: 'Doc_Num', sortable: true, filter: true },
    { headerName:'Chantier',field: 'Doc_RS', sortable: true, filter: true },
    { headerName:'Date',field: 'Doc_Date', sortable: true, filter: true },
    { headerName:'Montant facture',field: 'Doc_TTTC', sortable: true, filter: true }
  ];
  
  gridOptions: GridOptions = { groupIncludeFooter: true, groupIncludeTotalFooter: true };
  public rowData: Reglement[] = [];

  constructor(
    public dialogRef: MatDialogRef<ListeFagComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private fb: FormBuilder,
    private listeFagService: listeFagService,
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
    const totalDoc_TTTC = parseFloat(this.rowData.reduce((sum, row) => sum + row.Doc_TTTC, 0).toFixed(3));
    
    this.totalFooterRow = {
      Doc_Num: 'Total',
      Doc_RS: '',
      Doc_Date: '',
      Doc_TTTC: totalDoc_TTTC,
    };
    this.rowData = [...this.rowData, this.totalFooterRow];
  }
 
  async fetchModeRegFact(): Promise<void> {
    if (this.Fact_num) {
      try {
        const data = await this.listeFagService.getlisteFag(this.Fact_num);
        this.PaimentFact = data.ModePaiement || [];
        this.rowData = data.ModePaiement || [];
        this.calculateTotals(); // Recalculate totals after data fetch
      } catch (error) {
        console.error('Error fetching Liste Facture FAG for Fact_num:', error);
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
