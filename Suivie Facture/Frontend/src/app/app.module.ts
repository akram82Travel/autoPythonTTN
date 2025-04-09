import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MatListModule } from '@angular/material/list'; // Import MatListModule
import { MatIconModule } from '@angular/material/icon'; // Import MatIconModule
import { MatSidenavModule } from '@angular/material/sidenav'; // Import MatSidenavModule
import { MatTableModule } from '@angular/material/table'; // Import MatTableModule
import { MatSortModule } from '@angular/material/sort';   // Import MatSortModule
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatPaginatorModule } from '@angular/material/paginator';  // Import MatPaginatorModule
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatToolbarModule } from '@angular/material/toolbar'; // Import MatToolbarModule
import { MatButtonModule } from '@angular/material/button'; // Import MatButtonModule
import { AgGridModule } from 'ag-grid-angular'; // AG Grid module
import { MatDialogModule } from '@angular/material/dialog'; // Import MatDialogModule
import { MatSelectModule } from '@angular/material/select';
import { RouterModule, Routes } from '@angular/router'; // Import RouterModule
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { HttpClientModule } from '@angular/common/http';

import { SettingsDialogComponent } from './settings-dialog/settings-dialog.component';
import { ListeReglementComponent } from './liste-reglement/liste-reglement.component';
import { ListeFagComponent } from './liste-fag/liste-fag.component'; // Import your dialog component


// Define routes outside the imports array
const appRoutes: Routes = [
  { path: '', component: HomeComponent },
];

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    SettingsDialogComponent,
    ListeReglementComponent,
    ListeFagComponent  // Declare the dialog component
  ],
  imports: [
    BrowserModule,
    MatIconModule,
    MatListModule,
    MatSidenavModule,
    MatTableModule,
    MatSortModule,
    BrowserAnimationsModule,
    MatToolbarModule, // Include MatToolbarModule
    MatButtonModule, // Include MatButtonModule
    MatIconModule,
    MatPaginatorModule,
    HttpClientModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    AgGridModule,  // AG Grid initialized her
    MatDialogModule,
    FormsModule,
        ReactiveFormsModule,
    RouterModule.forRoot(appRoutes)  // Use the appRoutes constant here
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
