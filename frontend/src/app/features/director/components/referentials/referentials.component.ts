import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { MatTableModule } from '@angular/material/table';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';
import { MatMenuModule } from '@angular/material/menu';
import { MatChipsModule } from '@angular/material/chips';
import { DirectorService } from '../../services/director.service';
import { GroupFormDialogComponent } from './group-form-dialog.component';
import { Subject, Group } from '../../models/director.models';
import { FilterPipe } from '../../pipes/filter.pipe';
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { MatDividerModule } from '@angular/material/divider';
import { MatProgressBarModule } from '@angular/material/progress-bar';


@Component({
  selector: 'app-referentials',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTabsModule,
    MatTableModule,
    MatDialogModule,
    MatSnackBarModule,
    MatMenuModule,
    MatChipsModule,
  FilterPipe,
    MatProgressSpinnerModule,
    MatDividerModule,
    MatProgressBarModule
],
  templateUrl: './referentials.component.html',
  styleUrls: ['./referentials.component.css']
})
export class ReferentialsComponent implements OnInit {
  subjects: Subject[] = [];
  groups: Group[] = [];
  loading = true;
  
  subjectColumns: string[] = ['code', 'name', 'credits', 'semester', 'prerequisites', 'actions'];
  groupColumns: string[] = ['code', 'name', 'semester', 'students', 'capacity', 'subjects', 'actions'];

  constructor(
    private directorService: DirectorService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadSubjects();
    this.loadGroups();
  }

  loadSubjects() {
    this.loading = true;
    this.directorService.getSubjects('dept-1').subscribe({
      next: (subjects) => {
        this.subjects = subjects;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading subjects:', error);
        this.loading = false;
        // Mock data for demonstration
        this.subjects = [
          {
            id: '1',
            name: 'Mathématiques Générales',
            code: 'MATH101',
            credits: 6,
            semester: 1,
            departmentId: 'dept-1',
            description: 'Introduction aux mathématiques appliquées',
            prerequisites: []
          },
          {
            id: '2',
            name: 'Programmation Java',
            code: 'INFO201',
            credits: 4,
            semester: 2,
            departmentId: 'dept-1',
            description: 'Programmation orientée objet avec Java',
            prerequisites: ['MATH101']
          },
          {
            id: '3',
            name: 'Base de Données',
            code: 'INFO301',
            credits: 5,
            semester: 3,
            departmentId: 'dept-1',
            description: 'Conception et gestion de bases de données',
            prerequisites: ['INFO201']
          }
        ];
      }
    });
  }

  loadGroups() {
    this.directorService.getGroups('dept-1').subscribe({
      next: (groups) => {
        this.groups = groups;
      },
      error: (error) => {
        console.error('Error loading groups:', error);
        // Mock data for demonstration
        this.groups = [
          {
            id: '1',
            name: 'Groupe A - L1 Info',
            code: 'L1-INFO-A',
            departmentId: 'dept-1',
            semester: 1,
            studentCount: 28,
            maxCapacity: 30,
            subjects: ['MATH101', 'INFO101', 'PHYS101']
          },
          {
            id: '2',
            name: 'Groupe B - L1 Info',
            code: 'L1-INFO-B',
            departmentId: 'dept-1',
            semester: 1,
            studentCount: 25,
            maxCapacity: 30,
            subjects: ['MATH101', 'INFO101', 'PHYS101']
          },
          {
            id: '3',
            name: 'Groupe A - L2 Info',
            code: 'L2-INFO-A',
            departmentId: 'dept-1',
            semester: 3,
            studentCount: 32,
            maxCapacity: 35,
            subjects: ['INFO201', 'INFO301', 'MATH201']
          }
        ];
      }
    });
  }

  // Subject Management
  createSubject() {
    // Quick-create using prompts to avoid adding a full subject form component
    const name = prompt('Nom de la matière:');
    if (!name) return;
    const code = prompt('Code de la matière:', 'NEWCODE') || '';
    const creditsStr = prompt('Crédits (nombre):', '3') || '3';
    const semesterStr = prompt('Semestre (nombre):', '1') || '1';
    const credits = parseInt(creditsStr, 10) || 0;
    const semester = parseInt(semesterStr, 10) || 1;

    const payload: any = {
      name: name.trim(),
      code: code.trim(),
      credits,
      semester,
      departmentId: 'dept-1'
    };

    this.directorService.createSubject(payload).subscribe({
      next: () => {
        this.showMessage('Matière créée avec succès');
        this.loadSubjects();
      },
      error: () => this.showMessage('Erreur lors de la création de la matière')
    });
  }

  editSubject(subject: Subject) {
    // Simple inline edit via prompts for demo purposes
    const name = prompt('Nom de la matière:', subject.name);
    if (name === null) return;
    const code = prompt('Code de la matière:', subject.code) || subject.code;
    const creditsStr = prompt('Crédits (nombre):', String(subject.credits)) || String(subject.credits);
    const semesterStr = prompt('Semestre (nombre):', String(subject.semester)) || String(subject.semester);
    const credits = parseInt(creditsStr, 10) || subject.credits;
    const semester = parseInt(semesterStr, 10) || subject.semester;

    const payload: any = {
      name: name.trim(),
      code: code.trim(),
      credits,
      semester
    };

    this.directorService.updateSubject(subject.id, payload).subscribe({
      next: () => {
        this.showMessage('Matière mise à jour');
        this.loadSubjects();
      },
      error: () => this.showMessage('Erreur lors de la mise à jour')
    });
  }

  deleteSubject(subject: Subject) {
    if (confirm(`Êtes-vous sûr de vouloir supprimer la matière "${subject.name}" ?`)) {
      this.directorService.deleteSubject(subject.id).subscribe({
        next: () => {
          this.showMessage('Matière supprimée avec succès');
          this.loadSubjects();
        },
        error: (error) => {
          this.showMessage('Erreur lors de la suppression');
        }
      });
    }
  }

  // Group Management
  createGroup() {
    // Open the GroupFormDialog and create the group when closed
    const dialogRef = this.dialog.open(GroupFormDialogComponent, {
      width: '420px'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (!result) return;
      this.directorService.createGroup(result).subscribe({
        next: () => {
          this.showMessage('Groupe créé avec succès');
          this.loadGroups();
        },
        error: () => this.showMessage('Erreur lors de la création du groupe')
      });
    });
  }

  editGroup(group: Group) {
    // Simple inline edit via prompts; using dialog would require adapting GroupFormDialog to accept data
    const name = prompt('Nom du groupe:', group.name);
    if (name === null) return;
    const code = prompt('Code du groupe:', group.code) || group.code;
    const semesterStr = prompt('Semestre (nombre):', String(group.semester)) || String(group.semester);
    const maxCapacityStr = prompt('Capacité maximale:', String(group.maxCapacity)) || String(group.maxCapacity);

    const payload: any = {
      name: name.trim(),
      code: code.trim(),
      semester: parseInt(semesterStr, 10) || group.semester,
      maxCapacity: parseInt(maxCapacityStr, 10) || group.maxCapacity
    };

    this.directorService.updateGroup(group.id, payload).subscribe({
      next: () => {
        this.showMessage('Groupe mis à jour');
        this.loadGroups();
      },
      error: () => this.showMessage('Erreur lors de la mise à jour du groupe')
    });
  }

  deleteGroup(group: Group) {
    if (confirm(`Êtes-vous sûr de vouloir supprimer le groupe "${group.name}" ?`)) {
      this.directorService.deleteGroup(group.id).subscribe({
        next: () => {
          this.showMessage('Groupe supprimé avec succès');
          this.loadGroups();
        },
        error: (error) => {
          this.showMessage('Erreur lors de la suppression');
        }
      });
    }
  }

  viewGroupDetails(group: Group) {
    this.showMessage(`Détails du groupe: ${group.name}`);
  }

  viewSubjectDetails(subject: Subject) {
    this.showMessage(`Détails de la matière: ${subject.name} (${subject.code})`);
  }

  manageGroupStudents(group: Group) {
    // Placeholder: navigate to a student management page or show a message
    this.showMessage(`Gérer les étudiants pour ${group.name} (à implémenter)`);
  }

  openGroupTimetable(group: Group) {
    // Placeholder: navigate to group timetable view
    this.showMessage(`Ouvrir emploi du temps pour ${group.name} (à implémenter)`);
  }

  getCapacityColor(group: Group): string {
    const ratio = group.studentCount / group.maxCapacity;
    if (ratio >= 0.9) return 'warn';
    if (ratio >= 0.8) return 'accent';
    return 'primary';
  }

  getCapacityPercentage(group: Group): number {
    return (group.studentCount / group.maxCapacity) * 100;
  }

  getSemesterLabel(semester: number): string {
    switch (semester) {
      case 1: return 'S1';
      case 2: return 'S2';
      case 3: return 'S3';
      case 4: return 'S4';
      case 5: return 'S5';
      case 6: return 'S6';
      default: return `S${semester}`;
    }
  }

  // Statistical methods
  getTotalStudents(): number {
    return this.groups.reduce((sum, group) => sum + group.studentCount, 0);
  }

  getTotalCapacity(): number {
    return this.groups.reduce((sum, group) => sum + group.maxCapacity, 0);
  }

  getOccupancyRate(): number {
    const totalStudents = this.getTotalStudents();
    const totalCapacity = this.getTotalCapacity();
    return totalCapacity > 0 ? (totalStudents / totalCapacity) * 100 : 0;
  }

  getTotalCredits(): number {
    return this.subjects.reduce((sum, subject) => sum + subject.credits, 0);
  }

  getAverageCredits(): number {
    const totalCredits = this.getTotalCredits();
    return this.subjects.length > 0 ? totalCredits / this.subjects.length : 0;
  }

  private showMessage(message: string) {
    this.snackBar.open(message, 'Fermer', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'bottom'
    });
  }
}
