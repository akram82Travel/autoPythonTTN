import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Form } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})

export class reglementFatService {
  private apiUrl = 'http://127.0.0.1:8000/GetReglementFact';
  //private apiUrl2 = 'http://127.0.0.1:8000/ListModeReg';
  //private apiUrl3 = 'http://127.0.0.1:8000/SaveModePaiementFact';

  constructor(private http: HttpClient) { }

  /*getmodePaiement(): Observable<string[]> {
    return this.http.get<string[]>(this.apiUrl);
  }*/
  
  async getregFact(Fact_num: string): Promise<any> {
    const body = { FCT_num: Fact_num };
    try {
      const response = await this.http.post<any>(this.apiUrl, body).toPromise();

      if (!response) {
        throw new Error('Response is undefined');
      }
      return response;
    } catch (error) {
      console.error('Error in getOfs:', error);
      throw error;
    }
  }
  // Use Observable instead of Promise
  /*saveModePaiement(Fact_num: string, formData: any): Observable<any> {
    const body = { Fact_num: Fact_num, formData: formData };
    
    return this.http.post<any>(this.apiUrl3, body);
  }*/
}
