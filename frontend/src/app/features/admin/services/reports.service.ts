import { Injectable } from '@angular/core';
import { ApiService } from '../../../core/services/api.service';
import { Observable } from 'rxjs';

export interface AdminReport {
  id: string;
  title: string;
  createdAt: string;
  status: 'pending' | 'completed' | 'failed';
  data?: any;
}

@Injectable({ providedIn: 'root' })
export class ReportsService {
  constructor(private api: ApiService) {}

  // List previously generated reports (if backend supports)
  listReports(): Observable<AdminReport[]> {
    return this.api.get<AdminReport[]>('/admin/reports');
  }

  // Generate a report by calling analytics or referentiel exports
  generateReport(payload: { type: string; params?: any }): Observable<AdminReport> {
    // Example: type 'absences' -> call analytics aggregate or create a report job
    return this.api.post<AdminReport>('/admin/reports', payload);
  }

  getReport(id: string): Observable<AdminReport> {
    return this.api.get<AdminReport>(`/admin/reports/${id}`);
  }

  // Helper to download student CSV (referentiel service provides /etudiants/export)
  downloadStudentsCsv(): Observable<Blob> {
    return this.api.get<Blob>('/etudiants/export', undefined, { responseType: 'blob' });
  }
}
