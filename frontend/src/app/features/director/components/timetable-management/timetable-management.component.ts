import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { MatChipsModule } from '@angular/material/chips';
import { MatMenuModule } from '@angular/material/menu';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';
import { DirectorService } from '../../services/director.service';
import { Router } from '@angular/router';
import { TimetableCreatorService } from '../timetable-creator/timetable-creator.service';
import { Timetable, TimetableConflict } from '../../models/director.models';

@Component({
  selector: 'app-timetable-management',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTableModule,
    MatTabsModule,
    MatDialogModule,
    MatChipsModule,
    MatMenuModule,
    MatProgressSpinnerModule,
    MatSnackBarModule
  ],
  templateUrl: './timetable-management.component.html',
  styleUrls: ['./timetable-management.component.css']
})
export class TimetableManagementComponent implements OnInit {
  timetables: Timetable[] = [];
  conflicts: TimetableConflict[] = [];
  loading = true;
  creating = false;
  
  displayedColumns: string[] = ['subject', 'group', 'teacher', 'time', 'room', 'status', 'actions'];
  conflictColumns: string[] = ['type', 'description', 'severity', 'actions'];
  
  daysOfWeek = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
  timeSlots = [
    '08:30-10:00', '10:10-11:40', '11:50-13:20',
    '14:30-16:00', '16:10-17:40'
  ];

  weeklyView: any[][] = [];

  constructor(
    private directorService: DirectorService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar,
    private router: Router,
    private creatorService: TimetableCreatorService
  ) {}

  ngOnInit() {
    this.loadTimetables();
    this.loadConflicts();
  }

  loadTimetables() {
    this.loading = true;
    this.directorService.getTimetables('dept-1').subscribe({
      next: (timetables) => {
        this.timetables = timetables;
        this.generateWeeklyView();
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading timetables:', error);
        this.loading = false;
        this.showMessage('Erreur lors du chargement des emplois du temps');
      }
    });
  }

  loadConflicts() {
    this.directorService.getTimetableConflicts('dept-1').subscribe({
      next: (conflicts) => {
        this.conflicts = conflicts;
      },
      error: (error) => {
        console.error('Error loading conflicts:', error);
      }
    });
  }

  generateWeeklyView() {
    this.weeklyView = [];
    
    this.timeSlots.forEach(timeSlot => {
      const row: any[] = [timeSlot];
      
      this.daysOfWeek.forEach((day, dayIndex) => {
        const dayTimetables = this.timetables.filter(t => 
          t.dayOfWeek === dayIndex && 
          this.getTimeSlot(t.startTime, t.endTime) === timeSlot
        );
        row.push(dayTimetables);
      });
      
      this.weeklyView.push(row);
    });
  }

  getTimeSlot(startTime: string, endTime: string): string {
    return `${startTime}-${endTime}`;
  }

  getStatusColor(status: string): string {
    switch (status) {
      case 'VALIDATED': return 'primary';
      case 'PROPOSED': return 'accent';
      case 'REJECTED': return 'warn';
      case 'CONFLICT': return 'warn';
      default: return '';
    }
  }

  getConflictSeverityColor(severity: string): string {
    switch (severity) {
      case 'HIGH': return 'warn';
      case 'MEDIUM': return 'accent';
      case 'LOW': return 'primary';
      default: return '';
    }
  }

  validateTimetable(timetable: Timetable) {
    this.directorService.validateTimetable(timetable.id).subscribe({
      next: () => {
        this.showMessage('Emploi du temps validé avec succès');
        this.loadTimetables();
      },
      error: (error) => {
        this.showMessage('Erreur lors de la validation');
      }
    });
  }

  rejectTimetable(timetable: Timetable) {
    const reason = prompt('Raison du rejet:');
    if (reason) {
      this.directorService.rejectTimetable(timetable.id, reason).subscribe({
        next: () => {
          this.showMessage('Emploi du temps rejeté');
          this.loadTimetables();
        },
        error: (error) => {
          this.showMessage('Erreur lors du rejet');
        }
      });
    }
  }

  editTimetable(timetable: Timetable) {
    // Minimal edit: allow changing room and time for demo purposes
    const newRoom = prompt('Nouvelle salle:', timetable.roomId) || timetable.roomId;
    const newStart = prompt('Nouvelle heure de début (HH:mm):', timetable.startTime) || timetable.startTime;
    const newEnd = prompt('Nouvelle heure de fin (HH:mm):', timetable.endTime) || timetable.endTime;

    const payload: any = {
      roomId: newRoom.trim(),
      startTime: newStart.trim(),
      endTime: newEnd.trim()
    };

    this.directorService.updateTimetable(timetable.id, payload).subscribe({
      next: () => {
        this.showMessage('Emploi du temps mis à jour');
        this.loadTimetables();
      },
      error: () => this.showMessage('Erreur lors de la mise à jour')
    });
  }

  deleteTimetable(timetable: Timetable) {
    if (!confirm(`Supprimer l'emploi du temps pour ${timetable.subjectId} ?`)) return;
    this.directorService.deleteTimetable(timetable.id).subscribe({
      next: () => {
        this.showMessage('Emploi du temps supprimé');
        this.loadTimetables();
      },
      error: () => this.showMessage('Erreur lors de la suppression')
    });
  }

  resolveConflict(conflict: TimetableConflict) {
    // Ouvrir un dialogue pour résoudre le conflit
    this.showMessage('Fonctionnalité de résolution de conflit à implémenter');
  }

  createNewTimetable() {
    // Navigate immediately for snappier UX, then fetch groups in background.
    // Provide an empty initial value so the creator page can render.
    this.creatorService.setInitialGroups([]);
    this.creating = true;
    this.router.navigateByUrl('/director/timetable/create');

    this.directorService.getGroups('dept-1').subscribe({
      next: (groups) => {
        this.creatorService.setInitialGroups(groups || []);
        this.creating = false;
      },
      error: (err) => {
        this.creating = false;
        this.showMessage('Impossible de récupérer les groupes.');
      }
    });
  }

  exportTimetable() {
    this.showMessage('Export en cours...');
    // Logique d'export à implémenter
  }

  private showMessage(message: string) {
    this.snackBar.open(message, 'Fermer', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'bottom'
    });
  }
}
