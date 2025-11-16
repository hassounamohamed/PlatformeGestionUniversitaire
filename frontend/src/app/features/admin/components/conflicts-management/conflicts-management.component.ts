import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Conflict {
  id: number;
  description: string;
  timetableId: number;
  severity: 'low' | 'medium' | 'high';
}

@Component({
  selector: 'admin-conflicts-management',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './conflicts-management.component.html',
  styleUrls: ['../../pages/admin-dashboard/admin-dashboard.component.css']
})
export class ConflictsManagementComponent {
  conflicts: Conflict[] = [
    { id: 1, description: 'Double réservation salle A - 10:00', timetableId: 1, severity: 'high' },
    { id: 2, description: 'Conflit enseignant horaires', timetableId: 2, severity: 'medium' }
  ];

  resolve(id: number) {
    this.conflicts = this.conflicts.filter(c => c.id !== id);
    // TODO: call backend API to mark resolved
  }
}
