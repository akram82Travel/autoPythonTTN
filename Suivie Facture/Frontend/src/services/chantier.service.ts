import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChantierService {
  private apiUrl = 'http://127.0.0.1:8000/Chantier';

  constructor(private http: HttpClient) { }

  getChantiers(): Observable<string[]> {
    return this.http.get<string[]>(this.apiUrl);
  }
}
