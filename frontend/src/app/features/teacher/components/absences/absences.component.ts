import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatChipsModule } from '@angular/material/chips';
import { AbsenceService, AbsenceDto } from '../../../../core/services/absence.service';
import { AuthService } from '../../../../core/auth/services/auth.service';

interface Course {
  id: string;
  subject: string;
  group: string;
  time: string;
}

interface Absence {
  id: string;
  date: Date;
  startTime: string;
  endTime: string;
  course: string;
  reason: string;
  comment?: string;
  status: 'pending' | 'approved' | 'rejected';
  hasJustification?: boolean;
}

interface StudentAbsence extends Absence {
  studentName: string;
}

@Component({
  selector: 'app-absences',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTabsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatChipsModule
  ],
  templateUrl: './absences.component.html',
  styleUrl: './absences.component.css'
})
export class AbsencesComponent implements OnInit {
  selectedTab = 0;
  absenceForm: FormGroup;
  isSubmitting = false;
  selectedFile: File | null = null;
  selectedPeriod = 'month';
  selectedCourseFilter = '';

  myCourses: Course[] = [
    {
      id: '1',
      subject: 'Mathématiques Appliquées',
      group: 'L2 Info A',
      time: '08:30 - 10:00'
    },
    {
      id: '2',
      subject: 'Algorithmique',
      group: 'L1 Info B',
      time: '10:15 - 11:45'
    },
    {
      id: '3',
      subject: 'Base de Données',
      group: 'L2 Info A',
      time: '14:00 - 15:30'
    },
    {
      id: '4',
      subject: 'Programmation Web',
      group: 'L3 Info',
      time: '15:45 - 17:15'
    }
  ];

  myAbsences: Absence[] = [];

  pendingStudentAbsences: StudentAbsence[] = [];

  constructor(private fb: FormBuilder, private absenceService: AbsenceService, private auth: AuthService) {
    this.absenceForm = this.fb.group({
      date: ['', Validators.required],
      startTime: ['', Validators.required],
      endTime: ['', Validators.required],
      courseId: ['', Validators.required],
      reason: ['', Validators.required],
      comment: ['']
    });
  }

  ngOnInit(): void {
    this.loadAbsences();
  }

  private loadAbsences(): void {
    this.absenceService.listAbsences().subscribe({
      next: (res: AbsenceDto[]) => {
        // teacher sees own absences + pending student absences (filter by statut)
        this.myAbsences = [];
        this.pendingStudentAbsences = res
          .filter(r => (r.statut || '').toLowerCase() === 'pending')
          .map(r => ({
            id: String(r.id),
            studentName: `student-${r.etudiant_id}`,
            date: new Date(),
            startTime: '',
            endTime: '',
            course: '',
            reason: r.motif || '',
            comment: '',
            status: 'pending',
            hasJustification: false
          } as StudentAbsence));
      },
      error: (err: any) => console.error('Failed loading absences for teacher', err)
    });
  }

  onTabChange(event: any): void {
    this.selectedTab = event.index;
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
    }
  }

  submitAbsence(): void {
    if (this.absenceForm.valid) {
      this.isSubmitting = true;
      
      // Simulate API call
      setTimeout(() => {
        console.log('Absence submitted:', this.absenceForm.value);
        this.isSubmitting = false;
        this.resetForm();
        // Show success message
      }, 2000);
    }
  }

  resetForm(): void {
    this.absenceForm.reset();
    this.selectedFile = null;
  }

  filterMyAbsences(): void {
    // Filter absences based on selected period
    console.log('Filter my absences by period:', this.selectedPeriod);
  }

  filterStudentAbsences(): void {
    // Filter student absences based on selected course
    console.log('Filter student absences by course:', this.selectedCourseFilter);
  }

  cancelAbsence(absenceId: string): void {
    console.log('Cancel absence:', absenceId);
    // Remove from myAbsences array or update status
  }

  approveAbsence(absenceId: string): void {
    console.log('Approve absence:', absenceId);
    // Update absence status to approved
  }

  rejectAbsence(absenceId: string): void {
    console.log('Reject absence:', absenceId);
    // Update absence status to rejected
  }

  viewJustification(absenceId: string): void {
    console.log('View justification for absence:', absenceId);
    // Open justification document
  }

  getReasonLabel(reason: string): string {
    const reasons: { [key: string]: string } = {
      medical: 'Raison médicale',
      family: 'Raison familiale',
      professional: 'Raison professionnelle',
      transport: 'Problème de transport',
      other: 'Autre'
    };
    return reasons[reason] || reason;
  }

  getStatusLabel(status: string): string {
    const statuses: { [key: string]: string } = {
      pending: 'En attente',
      approved: 'Approuvée',
      rejected: 'Refusée'
    };
    return statuses[status] || status;
  }

  getStatusColor(status: string): string {
    const colors: { [key: string]: string } = {
      pending: 'accent',
      approved: 'primary',
      rejected: 'warn'
    };
    return colors[status] || 'accent';
  }
}
