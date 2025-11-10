import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export interface RattrapageCreateDto {
  absence_id: number;
  date: string; // YYYY-MM-DD
  heure_debut: string; // HH:MM:SS
  heure_fin: string; // HH:MM:SS
  salle_id?: number | null;
}

@Injectable({ providedIn: 'root' })
export class RattrapageService {
  private path = '/rattrapages';

  constructor(private api: ApiService) {}

  createRattrapage(payload: RattrapageCreateDto): Observable<any> {
    return this.api.post<any>(this.path, payload);
  }

  listRattrapages(): Observable<any[]> {
    return this.api.get<any[]>(this.path);
  }
}
