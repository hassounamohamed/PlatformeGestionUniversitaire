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
    // Direct call to absence service (local dev port 8007)
    return this.api.get<AbsenceDto[]>('http://127.0.0.1:8007/absences');
  }

  getAbsence(id: number) {
    return this.api.get<AbsenceDto>(`http://127.0.0.1:8007/absences/${id}`);
  }

  createAbsence(payload: Partial<AbsenceDto>) {
    return this.api.post<AbsenceDto>('http://127.0.0.1:8007/absences', payload);
  }

  updateAbsence(id: number, patch: Partial<AbsenceDto>) {
    // Backend exposes PATCH for partial updates
    return this.api.patch<AbsenceDto>(`http://127.0.0.1:8007/absences/${id}`, patch);
  }

  deleteAbsence(id: number) {
    return this.api.delete<AbsenceDto>(`http://127.0.0.1:8007/absences/${id}`);
  }
}
