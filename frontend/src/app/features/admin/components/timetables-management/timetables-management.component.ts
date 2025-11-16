import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Timetable {
  id: number;
  name: string;
  owner: string;
  lastUpdated: string;
}

@Component({
  selector: 'admin-timetables-management',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './timetables-management.component.html',
  styleUrls: ['../../pages/admin-dashboard/admin-dashboard.component.css']
})
export class TimetablesManagementComponent {
  timetables: Timetable[] = [
    { id: 1, name: 'Semestre 1 - CS', owner: 'Département CS', lastUpdated: '2025-10-10' },
    { id: 2, name: 'Semestre 1 - Math', owner: 'Département Math', lastUpdated: '2025-10-12' }
  ];

  edit(id: number) {
    console.log('edit', id);
  }

  delete(id: number) {
    this.timetables = this.timetables.filter(t => t.id !== id);
  }

  assign(id: number) {
    console.log('assign', id);
  }
}
