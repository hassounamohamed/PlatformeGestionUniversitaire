import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { AbsenceService, AbsenceDto } from '../../../../core/services/absence.service';
import { AuthService } from '../../../../core/auth/services/auth.service';

interface ViewAbsence {
  id: number;
  date: string;
  course?: string;
  status?: string;
}

@Component({
  selector: 'app-student-absences',
  standalone: true,
  imports: [CommonModule, DatePipe, MatButtonModule],
  templateUrl: './absences.component.html',
  styleUrls: ['./absences.component.css']
})
export class AbsencesComponent implements OnInit {
  absences: ViewAbsence[] = [];
  loading = false;

  constructor(private absenceService: AbsenceService, private auth: AuthService) {}

  ngOnInit(): void {
    this.loadMyAbsences();
  }

  private loadMyAbsences(): void {
    const user = this.auth.getCurrentUser();
    if (!user) return;
    this.loading = true;
    this.absenceService.listAbsences().subscribe({
      next: (res: AbsenceDto[]) => {
        // Backend returns AbsenceDto with etudiant_id — filter client-side
        this.absences = res
          .filter((a: AbsenceDto) => a.etudiant_id === (user as any).id)
          .map((a: AbsenceDto) => ({ id: a.id, date: new Date().toISOString(), course: '', status: a.statut || 'unknown' }));
        // try to format date from related emploi_id later if available
        this.loading = false;
      },
      error: (err: any) => {
        console.error('Failed loading absences', err);
        this.loading = false;
      }
    });
  }

  requestExcuse(abs: ViewAbsence) {
    // Navigate to create justificatif or open a dialog in a separate change.
    console.log('Requesting excuse for', abs);
  }
}
