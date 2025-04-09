import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TicketService {
  private apiUrl = 'http://127.0.0.1:8000/Ticket';

  constructor(private http: HttpClient) { }

  async getTickets(of_num: string): Promise<any> {
    const body = { OF_num: of_num };
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
