import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { modePaiementService } from '../../services/modePaiement.service';

import { ActivatedRoute, Router } from '@angular/router';
@Component({
  selector: 'app-settings-dialog',
  templateUrl: './settings-dialog.component.html',
})
export class SettingsDialogComponent {
  paymentForm: FormGroup;
  dataSource: any[] = [];
  dataSourcefact: any[] = [];
  Fact_num: string = '';
  PaimentFact: any[] = [];
  selectedMethod: string =  '';
/*
  PaimentFact: any = {
    numFacture: '',
    codeMode: '',
    avance: '',
    reception: '',
    pose: '',
    finmarche: ''
  };
*/

  facture: any;
  constructor(
    public dialogRef: MatDialogRef<SettingsDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,  // Inject the data passed from the parent component

    private fb: FormBuilder,
    private modePaiementService: modePaiementService,
    private route: ActivatedRoute
  ) {
      this.facture = data.facture;  // Access the passed Facture object
      this.Fact_num = data.facture.Facture;  // Access the passed Facture object
      //liste des mode de paiement selon facture
      this.fetchModeRegFact();

      // Initialize the form group
      this.paymentForm = this.fb.group({
      standardMethod: [null], // Ensure selection is required
      advancePayment: [null, [Validators.required, Validators.min(0), Validators.max(999999)]], // Validate percentage
      dureePayment: [null, [Validators.required, Validators.min(0), Validators.max(999999)]], // Validate percentage
      receptionPayment: [null, [Validators.required, Validators.min(0), Validators.max(999999)]],
      postInstallationPayment: [null, [Validators.required, Validators.min(0), Validators.max(999999)]],
      endOfContractPayment: [null, [Validators.required, Validators.min(0), Validators.max(999999)]],
    });
  }
  
  ngOnInit(): void {
    //liste des mode de paiement
    this.modePaiementService.getmodePaiement().subscribe(
      (data: any) => {
        this.dataSource = data.ModePaiement || [];
        console.log('Success load liste mode');
        // Set the default value for the form control
      },
      (error) => {
        console.error('Error fetching ModePaiement:', error);
      }
    );
   
    
  }

  async fetchModeRegFact(): Promise<void> {
    if (this.Fact_num) {
      try {
        const data = await this.modePaiementService.getmodePaiementFact(this.Fact_num);
        this.PaimentFact = data.ModePaiement || [];
        console.log(data?.ModePaiement?.[0]?.codeMode);
        this.paymentForm = this.fb.group({
          standardMethod: [parseInt(data?.ModePaiement?.[0]?.codeMode) || null],
          advancePayment: [data?.ModePaiement?.[0]?.avance ?? null, [Validators.required, Validators.min(0), Validators.max(999999)]],
          dureePayment: [data?.ModePaiement?.[0]?.duree ?? null, [Validators.required, Validators.min(0), Validators.max(999999)]],
          receptionPayment: [data?.ModePaiement?.[0]?.reception ?? null, [Validators.required, Validators.min(0), Validators.max(999999)]],
          postInstallationPayment: [data?.ModePaiement?.[0]?.pose ?? null, [Validators.required, Validators.min(0), Validators.max(999999)]],
          endOfContractPayment: [data?.ModePaiement?.[0]?.finmarche ?? null, [Validators.required, Validators.min(0), Validators.max(999999)]],
        });
        console.log(this.PaimentFact);
      } catch (error) {
        console.error('Error fetching ModePaiement for Fact_num:', error);
      }

      
    }
  }


  onNoClick(): void {
    this.dialogRef.close();
  }

  // Save the form data when clicking "Edit"
  editModePaiement(): void {
    
    if (this.paymentForm.valid) {
      const formData = this.paymentForm.value;
      console.log('Form Data:', formData);

      // API call to save the data
      // Call the service to save data
    this.modePaiementService.saveModePaiement(this.facture.Facture, formData).subscribe(
      (response) => {
        console.log('Payment mode saved successfully:', response);
        alert('Payment mode saved successfully')
        this.dialogRef.close(formData); // Close the dialog and pass data
      },
      (error) => {
        alert()
        console.error('Error saving payment mode:', error);
      }
    );
  } else {
    console.log('Form Data:', this.paymentForm.value);
    console.warn('Form is invalid');
  }
  }
  
  

}
