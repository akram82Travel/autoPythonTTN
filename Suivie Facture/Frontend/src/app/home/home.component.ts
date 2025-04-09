import { Component, ViewChild, OnInit } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { CollapseService } from '../../services/collapse.service';
import { Router } from '@angular/router';
import { FactureTTNService } from '../../services/FactureTTN.service';
/* Core Data Grid CSS */
import 'ag-grid-community/styles/ag-grid.css';
/* Quartz Theme Specific CSS */
import 'ag-grid-community/styles/ag-theme-quartz.css';
import { ColDef, RowStyle } from 'ag-grid-community'; // Import the ColDef type
import { MatDialog } from '@angular/material/dialog';
import { SettingsDialogComponent } from '../settings-dialog/settings-dialog.component'; // Update the path as necessary
import { ListeReglementComponent } from '../liste-reglement/liste-reglement.component';
import { ListeFagComponent } from '../liste-fag/liste-fag.component';

// Define the interface for the data structure returned from the API
export interface Facture {
  Year: string; // Make sure the API returns a position if you're using it
  Facture: string;
  Date: Date;
  ModReglement: string;
  FAGDetail: string;
  ReglementFact: string;
  Montant: number;
  Devise: string;
  Beneficiaire: string;
  Chantier: string;
  TitreNum: number;
  DateDecla: string;
  Banque: string;
  NumDomiciliation: string;
  DDomiciliation: string;
  isParam: string;
  Decla_Num: string;

}


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent implements OnInit {
  FactureTTN: any[] = [];
  displayedColumns: string[] = ['Year', 'Facture', 'Date', 'ModReglement', 'ReglementFact', 'Montant','Devise','Beneficiaire', 'Chantier','TitreNum', 'NumDecla', 'DDecla','Banque', 'NumDomiciliation', 'DDomiciliation', 'isParam'];
  // AG Grid columns
  getRowStyle(params: any): RowStyle {
    return {
      backgroundColor: params.data.isParam ? 'lightgreen' : 'lightred' // Set color based on isParam
    };
  }
  columnDefs: ColDef<Facture>[] = [
    { 
      field: 'isParam', 
      sortable: true, 
      filter: true,
      width: 100, // Set the width of the cell to 20 pixels
      cellRenderer: (params: any) => {
          return params.data.isParam ? `
              <span class="ag-icon ag-icon-checkbox-checked" unselectable="on" role="presentation"></span>
          ` : '';
      }
  },
    { field: 'Year', sortable: true, filter: true,width: 100 },  // boolean value for filter
    { field: 'Facture', sortable: true, filter: true,width: 120 },  // boolean value for filter
    { field: 'Date', sortable: true, filter: 'agTextColumnFilter',width: 120 },  // filter by text
    { field: 'ModReglement',cellRenderer: (params: any) => {
      return `
       <button class="custom-btn">
            <span class="ag-icon ag-icon-eye" unselectable="on" role="presentation"></span>
          </button>
      `;
    },
    onCellClicked: (params: any) => {
      this.openSettingsDialog(params.data);  // Call the dialog when button is clicked
    }, sortable: true, filter: true, width: 120 },
    { field: 'ReglementFact',cellRenderer: (params: any) => {
      return `
       <button class="custom-btn">
            <span class="ag-icon ag-icon-eye" unselectable="on" role="presentation"></span>
          </button>
      `;
    },
    onCellClicked: (params: any) => {
      this.openRegFactsDialog(params.data);  // Call the dialog when button is clicked
    }, sortable: true, filter: true, width: 120 },
    { field: 'FAGDetail',cellRenderer: (params: any) => {
      return `
       <button class="custom-btn">
            <span class="ag-icon ag-icon-eye" unselectable="on" role="presentation"></span>
          </button>
      `;
    },
    onCellClicked: (params: any) => {
      this.openFAGDialog(params.data);  // Call the dialog when button is clicked
    }, sortable: true, filter: true, width: 120 },
    { headerName: 'Montant',field: 'Montant', sortable: true, filter: 'agNumberColumnFilter',width: 150  },  // using Date filter
    { field: 'Devise', sortable: true, filter: 'agNumberColumnFilter',width: 100 },  // using number filter
    { field: 'Beneficiaire', sortable: true, filter: true },
    { field: 'Chantier', sortable: true, filter: true },
    { field: 'TitreNum', sortable: true, filter: true,width: 120 },
    { headerName: 'Decla. Num',field: 'Decla_Num', sortable: true, filter: true,width: 120 },
    { field: 'DateDecla', sortable: true, filter: true,width: 120 },
    { field: 'Banque', sortable: true, filter: true,width: 120 },
    { field: 'NumDomiciliation', sortable: true, filter: true,width: 120 },
    { field: 'DDomiciliation', sortable: true, filter: true,width: 120 },
    
    
  ];

  public rowData: Facture[] = [];
  @ViewChild(MatSort, { static: true }) sort!: MatSort;
  @ViewChild(MatPaginator, { static: true }) paginator!: MatPaginator;

  filterValues: any = {
    Year: '',
    Beneficiaire: '',
    Chantier: '',
    Facture: '',
    ModReglement: '',
    ReglementFact: '',
    Date: '',
    Montant: '',
    TitreNum: '',
    Banque: '',
    Devise: '',
    isParam: '',
    Decla_Num_Imp: '',
    Decla_Num_Exp: ''
  };

  // Define the page size options
  pageSizeOptions: number[] = [13,20, 50, 100, 150, 200];
  dataSource = new MatTableDataSource<Facture>([]); // Initialize with an empty array
  constructor(
    private router: Router,
    public collapseService: CollapseService,
    private FactureTTNService: FactureTTNService,
  private dialog: MatDialog // Inject MatDialog
    
  ) {}
 
  
  ngOnInit() {
    this.dataSource.sort = this.sort;  // Attach sorting to the data source
    this.dataSource.paginator = this.paginator;  // Attach paginator to the data source
    this.FactureTTNService.getFactureTTN().subscribe(
      (data: any) => {
        this.dataSource.data = data.FactureTTN || [];
        this.rowData = data.FactureTTN || [];
        
      },
      (error) => {
        console.error('Error fetching Facture:', error);
      }
    );
  }
  onGridReady(params: any): void {
    // Automatically size columns to fit content
    const allColumnIds: string[] = [];
    if(params.length>0){
      params.columnApi.getAllColumns().forEach((column: any) => {
        allColumnIds.push(column.getColId());
      });
      params.columnApi.autoSizeColumns(allColumnIds);

    }
    
  }
  openSettingsDialog(facture: Facture): void {
    const dialogRef = this.dialog.open(SettingsDialogComponent, {
      width: '1250px',
      data: { facture }  // Pass the facture data to the dialog

    });
  
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      // Do something after the dialog closes if necessary
    });
  }
  
  openRegFactsDialog(facture: Facture): void {
    const dialogRef = this.dialog.open(ListeReglementComponent, {
      width: '1250px',
      data: { facture }  // Pass the facture data to the dialog

    });
  
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      // Do something after the dialog closes if necessary
    });
  }
  
  openFAGDialog(facture: Facture): void {
    const dialogRef = this.dialog.open(ListeFagComponent, {
      width: '1250px',
      data: { facture }  // Pass the facture data to the dialog

    });
  
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      // Do something after the dialog closes if necessary
    });
  }


  // Define pagination properties
  paginationPageSize: number = 13; // Set page size for pagination
    // Apply filter for the data table
    applyFilter(event: Event, column: string) {
      const filterValue = (event.target as HTMLInputElement).value.trim().toLowerCase();
      this.dataSource.filter = filterValue; // Filtering for Material Table
    }

}
