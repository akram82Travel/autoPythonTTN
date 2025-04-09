import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class OfService {
  private apiUrl = 'http://127.0.0.1:8000/ListOF/';

  constructor(private http: HttpClient) { }

  async getOfs(df_num: string, RefMarche: string): Promise<any> {
    const body = { DF_num: df_num, RefMarche:RefMarche };
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
}

