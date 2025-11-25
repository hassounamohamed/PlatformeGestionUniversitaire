import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class EmploiService {
  // Directly call the emploi service for local development
  private readonly API = 'http://127.0.0.1:8004/emplois';

  constructor(private http: HttpClient) {}

  private authHeaders(): { headers?: HttpHeaders } {
    const token = localStorage.getItem('auth_token');
    if (!token) return {};
    return { headers: new HttpHeaders({ Authorization: `Bearer ${token}` }) };
  }

  getEmploisByEnseignant(enseignantId: number) {
    const opts = this.authHeaders();
    return this.http.get<any[]>(`${this.API}/?enseignant_id=${enseignantId}`, opts);
  }

  getAllEmplois() {
    const opts = this.authHeaders();
    return this.http.get<any[]>(`${this.API}/`, opts);
  }

  /**
   * Fallback: request emplois by enseignant name (server will try to resolve name->id)
   */
  getEmploisByEnseignantName(name: string) {
    const opts = this.authHeaders();
    return this.http.get<any[]>(`${this.API}/?enseignant_nom=${encodeURIComponent(name)}`, opts);
  }
}
