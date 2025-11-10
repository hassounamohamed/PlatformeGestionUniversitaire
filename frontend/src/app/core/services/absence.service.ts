import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { AuthService } from '../auth/services/auth.service';

export interface AbsenceDto {
  id: number;
  etudiant_id: number;
  emploi_id?: number | null;
  motif?: string | null;
  statut?: string | null;
}

@Injectable({ providedIn: 'root' })
export class AbsenceService {
  constructor(private api: ApiService, private auth: AuthService) {}

  // Get all absences from backend. Filtering by student is done client-side using etudiant_id
  listAbsences(): Observable<AbsenceDto[]> {
    return this.api.get<AbsenceDto[]>('/absences');
  }

  getAbsence(id: number) {
    return this.api.get<AbsenceDto>(`/absences/${id}`);
  }

  createAbsence(payload: Partial<AbsenceDto>) {
    return this.api.post<AbsenceDto>('/absences', payload);
  }

  updateAbsence(id: number, patch: Partial<AbsenceDto>) {
    return this.api.put<AbsenceDto>(`/absences/${id}`, patch);
  }

  deleteAbsence(id: number) {
    return this.api.delete<AbsenceDto>(`/absences/${id}`);
  }
}
