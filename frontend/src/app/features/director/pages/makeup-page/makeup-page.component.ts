import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatChipsModule } from '@angular/material/chips';
import { MatMenuModule } from '@angular/material/menu';
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';
import { DirectorService } from '../../services/director.service';
import { MakeupSession } from '../../models/director.models';

@Component({
  selector: 'app-makeup-page',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTableModule,
    MatChipsModule,
    MatMenuModule,
    MatSnackBarModule
  ],
  template: `
    <div class="makeup-page">
      <!-- Floating Shapes Background -->
      <div class="floating-shapes" aria-hidden="true">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
      </div>

      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <h1>Gestion des Rattrapages</h1>
          <p class="subtitle">Approuver et organiser les séances de rattrapage</p>
          
        </div>
      </div>

      <!-- Content -->
      <div class="content-container">
        <mat-card class="makeup-card">
          <mat-card-header>
            <mat-icon mat-card-avatar>event_available</mat-icon>
            <mat-card-title>Demandes de Rattrapage</mat-card-title>
            <mat-card-subtitle>{{ makeupSessions.length }} séance(s) en attente</mat-card-subtitle>
          </mat-card-header>
          
          <mat-card-content>
            <div class="table-container">
              <table mat-table [dataSource]="makeupSessions" class="makeup-table">
                
                <ng-container matColumnDef="subject">
                  <th mat-header-cell *matHeaderCellDef>Matière</th>
                  <td mat-cell *matCellDef="let session">{{ session.subjectId }}</td>
                </ng-container>

                <ng-container matColumnDef="group">
                  <th mat-header-cell *matHeaderCellDef>Groupe</th>
                  <td mat-cell *matCellDef="let session">{{ session.groupId }}</td>
                </ng-container>

                <ng-container matColumnDef="teacher">
                  <th mat-header-cell *matHeaderCellDef>Enseignant</th>
                  <td mat-cell *matCellDef="let session">{{ session.teacherId }}</td>
                </ng-container>

                <ng-container matColumnDef="originalDate">
                  <th mat-header-cell *matHeaderCellDef>Date Originale</th>
                  <td mat-cell *matCellDef="let session">{{ session.originalDate | date:'dd/MM/yyyy HH:mm' }}</td>
                </ng-container>

                <ng-container matColumnDef="makeupDate">
                  <th mat-header-cell *matHeaderCellDef>Date Rattrapage</th>
                  <td mat-cell *matCellDef="let session">{{ session.makeupDate | date:'dd/MM/yyyy HH:mm' }}</td>
                </ng-container>

                <ng-container matColumnDef="reason">
                  <th mat-header-cell *matHeaderCellDef>Raison</th>
                  <td mat-cell *matCellDef="let session">
                    <div class="reason-text">{{ session.reason }}</div>
                  </td>
                </ng-container>

                <ng-container matColumnDef="status">
                  <th mat-header-cell *matHeaderCellDef>Statut</th>
                  <td mat-cell *matCellDef="let session">
                    <mat-chip [color]="getStatusColor(session.status)">
                      {{ getStatusLabel(session.status) }}
                    </mat-chip>
                  </td>
                </ng-container>

                <ng-container matColumnDef="actions">
                  <th mat-header-cell *matHeaderCellDef>Actions</th>
                  <td mat-cell *matCellDef="let session">
                    <button mat-icon-button [matMenuTriggerFor]="menu" color="primary">
                      <mat-icon>more_vert</mat-icon>
                    </button>
                    <mat-menu #menu="matMenu">
                      <button mat-menu-item 
                              *ngIf="session.status === 'REQUESTED'"
                              (click)="approveSession(session)">
                        <mat-icon color="primary">check</mat-icon>
                        <span>Approuver</span>
                      </button>
                      <button mat-menu-item 
                              *ngIf="session.status === 'REQUESTED'"
                              (click)="rejectSession(session)">
                        <mat-icon color="warn">close</mat-icon>
                        <span>Rejeter</span>
                      </button>
                      <button mat-menu-item (click)="editSession(session)">
                        <mat-icon>edit</mat-icon>
                        <span>Modifier</span>
                      </button>
                      <button mat-menu-item (click)="viewSession(session)">
                        <mat-icon>visibility</mat-icon>
                        <span>Détails</span>
                      </button>
                    </mat-menu>
                  </td>
                </ng-container>

                <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
                <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
              </table>
            </div>

            <div *ngIf="makeupSessions.length === 0" class="no-sessions">
              <mat-icon>event_available</mat-icon>
              <h3>Aucune séance de rattrapage</h3>
              <p>Aucune demande de rattrapage en attente pour le moment.</p>
            </div>
          </mat-card-content>
        </mat-card>
      </div>
    </div>
  `,
  styleUrls: ['./makeup-page.component.css']
})
export class MakeupPageComponent implements OnInit {
  makeupSessions: MakeupSession[] = [];
  displayedColumns: string[] = ['subject', 'group', 'teacher', 'originalDate', 'makeupDate', 'reason', 'status', 'actions'];

  constructor(
    private directorService: DirectorService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit() {
    this.loadMakeupSessions();
  }

  loadMakeupSessions() {
    this.directorService.getMakeupSessions('dept-1').subscribe({
      next: (sessions) => {
        this.makeupSessions = sessions;
      },
      error: (error) => {
        console.error('Error loading makeup sessions:', error);
        // Mock data pour la démonstration
        this.makeupSessions = [
          {
            id: '1',
            subjectId: 'MATH101',
            groupId: 'L1-INFO-A',
            teacherId: 'prof-martin',
            originalDate: new Date('2025-01-10T10:00:00'),
            makeupDate: new Date('2025-01-15T14:30:00'),
            reason: 'Enseignant malade',
            status: 'REQUESTED',
            roomId: 'A201',
            duration: 90
          },
          {
            id: '2',
            subjectId: 'INFO201',
            groupId: 'L2-INFO-A',
            teacherId: 'prof-durand',
            originalDate: new Date('2025-01-12T09:00:00'),
            makeupDate: new Date('2025-01-18T16:00:00'),
            reason: 'Panne électrique',
            status: 'APPROVED',
            roomId: 'B105',
            duration: 120
          }
        ];
      }
    });
  }

  approveSession(session: MakeupSession) {
    this.directorService.approveMakeupSession(session.id).subscribe({
      next: () => {
        this.showMessage('Séance de rattrapage approuvée');
        this.loadMakeupSessions();
      },
      error: (error) => {
        this.showMessage('Erreur lors de l\'approbation');
      }
    });
  }

  rejectSession(session: MakeupSession) {
    const reason = prompt('Raison du rejet:');
    if (reason) {
      this.directorService.rejectMakeupSession(session.id, reason).subscribe({
        next: () => {
          this.showMessage('Séance de rattrapage rejetée');
          this.loadMakeupSessions();
        },
        error: (error) => {
          this.showMessage('Erreur lors du rejet');
        }
      });
    }
  }

  createMakeupSession() {
    this.showMessage('Fonctionnalité de création de rattrapage à implémenter');
  }

  editSession(session: MakeupSession) {
    // Minimal edit flow: allow changing the makeup date via prompt for demo
    const current = session.makeupDate ? new Date(session.makeupDate).toISOString().slice(0,16) : '';
    const newDateStr = prompt('Nouvelle date de rattrapage (YYYY-MM-DDTHH:mm):', current);
    if (newDateStr === null) return;
    const newDate = new Date(newDateStr);
    if (isNaN(newDate.getTime())) {
      this.showMessage('Date invalide');
      return;
    }
    // No update endpoint implemented; show message and locally update for UX
    session.makeupDate = newDate;
    this.showMessage('Date modifiée (localement)');
  }

  viewSession(session: MakeupSession) {
    const details = `Matière: ${session.subjectId}\nGroupe: ${session.groupId}\nEnseignant: ${session.teacherId}\nDate rattrapage: ${session.makeupDate}`;
    this.showMessage(details);
  }

  getStatusColor(status: string): string {
    switch (status) {
      case 'APPROVED': return 'primary';
      case 'REQUESTED': return 'accent';
      case 'REJECTED': return 'warn';
      case 'COMPLETED': return 'primary';
      default: return '';
    }
  }

  getStatusLabel(status: string): string {
    switch (status) {
      case 'REQUESTED': return 'En Attente';
      case 'APPROVED': return 'Approuvé';
      case 'REJECTED': return 'Rejeté';
      case 'COMPLETED': return 'Terminé';
      default: return status;
    }
  }

  private showMessage(message: string) {
    this.snackBar.open(message, 'Fermer', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'bottom'
    });
  }
}