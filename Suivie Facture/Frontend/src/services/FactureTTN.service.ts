import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FactureTTNService {
  private apiUrl = 'http://127.0.0.1:8000/FactureTTN';

  constructor(private http: HttpClient) { }

  getFactureTTN(): Observable<string[]> {
    return this.http.get<string[]>(this.apiUrl);
  }
}
