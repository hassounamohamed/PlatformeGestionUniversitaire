import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatTooltipModule } from '@angular/material/tooltip';
import { AuthService } from '../../../../core/auth/services/auth.service';
import { EmploiService } from '../../../../core/services/emploi.service';

interface TimeSlot {
  start: string;
  end: string;
}

interface Day {
  name: string;
  date: Date;
}

interface Course {
  id: string;
  subject: string;
  group: string;
  room: string;
  type: 'lecture' | 'td' | 'tp';
  day: string;
  startTime: string;
  endTime: string;
}

interface WeeklyStats {
  totalHours: number;
  totalCourses: number;
  uniqueGroups: number;
}

interface Makeup {
  subject: string;
  date: Date;
  time: string;
  room: string;
}

@Component({
  selector: 'app-timetable',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatSelectModule,
    MatFormFieldModule,
    MatTooltipModule
  ],
  templateUrl: './timetable.component.html',
  styleUrls: ['./timetable.component.css']
})
export class TimetableComponent implements OnInit {
  selectedWeek = 'current';
  selectedSubject = '';

  weeks = [
    { value: 'previous', label: 'Semaine précédente' },
    { value: 'current', label: 'Semaine actuelle' },
    { value: 'next', label: 'Semaine prochaine' }
  ];

  subjects = [
    'Mathématiques Appliquées',
    'Algorithmique',
    'Base de Données',
    'Programmation Web'
  ];

  days: Day[] = [
    { name: 'Lundi', date: new Date('2025-10-14') },
    { name: 'Mardi', date: new Date('2025-10-15') },
    { name: 'Mercredi', date: new Date('2025-10-16') },
    { name: 'Jeudi', date: new Date('2025-10-17') },
    { name: 'Vendredi', date: new Date('2025-10-18') }
  ];

  timeSlots: TimeSlot[] = [
    { start: '08:30', end: '10:00' },
    { start: '10:10', end: '11:40' },
    { start: '11:50', end: '13:20' },
    { start: '14:30', end: '16:00' },
    { start: '16:10', end: '17:40' }
  ];
  // courses will be loaded from the backend (DB). Remove hard-coded samples.
  courses: Course[] = [];

  // initial stats are zero until we load courses from backend
  weeklyStats: WeeklyStats = {
    totalHours: 0,
    totalCourses: 0,
    uniqueGroups: 0
  };

  // upcoming makeups come from backend when available
  upcomingMakeups: Makeup[] = [];

  constructor(private auth: AuthService, private emploiService: EmploiService) {}
  ngOnInit(): void {
    this.calculateWeeklyStats();

    // 1) Prefer explicit current_user stored by the frontend (fast, works offline)
    const stored = localStorage.getItem('current_user');
    if (stored) {
      try {
        const u = JSON.parse(stored);
        this.loadEmploisForUser(u);
        return;
      } catch (e) {
        console.warn('Invalid current_user in localStorage, will try token/Auth.me()', e);
      }
    }

    // 2) Try to decode id from JWT token if present (fast fallback)
    const token = localStorage.getItem('auth_token');
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const id = payload?.id || payload?.sub;
        if (id) {
          // If payload.sub contains email, id may be a string; try numeric cast
          const numericId = Number(id) || undefined;
          if (numericId) {
            this.emploiService.getEmploisByEnseignant(numericId).subscribe({
              next: (items: any[]) => {
                this.courses = items.map(it => ({
                  id: String(it.id),
                  subject: it.matiere_nom || 'Cours',
                  group: it.groupe_nom || (it.groupe_id ? String(it.groupe_id) : ''),
                  room: it.salle && it.salle.numero ? String(it.salle.numero) : (it.salle_id ? String(it.salle_id) : ''),
                  type: 'lecture',
                  day: this.capitalize(new Date(it.date).toLocaleDateString('fr-FR', { weekday: 'long' })),
                  startTime: (it.heure_debut || '').substring(0,5),
                  endTime: (it.heure_fin || '').substring(0,5)
                }));
                this.calculateWeeklyStats();
              },
              error: (err) => console.error('Failed to load emplois by id from token', err)
            });
            return;
          }
        }
      } catch (e) {
        console.warn('Failed to decode token payload', e);
      }
    }

    // 3) Last resort: ask auth service for /me, then fallback to localStorage
    this.auth.me().subscribe({
      next: (u: any) => this.loadEmploisForUser(u),
      error: (err) => {
        console.warn('Could not get current user via /me, falling back to localStorage', err);
        try {
          const raw = localStorage.getItem('current_user');
          if (raw) {
            const u = JSON.parse(raw);
            this.loadEmploisForUser(u);
            return;
          }
        } catch (e) {
          console.warn('Failed to parse localStorage current_user', e);
        }
        // Nothing available — leave static data in place
      }
    });
  }

  private loadEmploisForUser(u: any) {
    if (!u) return;
    const id = u.id || (u && u.id);
    if (!id) return;
    this.emploiService.getEmploisByEnseignant(id).subscribe({
      next: (items: any[]) => {
        this.courses = items.map(it => ({
          id: String(it.id),
          subject: it.matiere_nom || 'Cours',
          group: it.groupe_nom || (it.groupe_id ? String(it.groupe_id) : ''),
          room: it.salle && it.salle.numero ? String(it.salle.numero) : (it.salle_id ? String(it.salle_id) : ''),
          type: 'lecture',
          day: this.capitalize(new Date(it.date).toLocaleDateString('fr-FR', { weekday: 'long' })),
          startTime: (it.heure_debut || '').substring(0,5),
          endTime: (it.heure_fin || '').substring(0,5)
        }));
        this.calculateWeeklyStats();
      },
      error: (err) => console.error('Failed to load emplois', err)
    });
  }

  private capitalize(str: string) {
    if (!str) return str;
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
  }

  getCourse(day: string, startTime: string): Course | null {
    return this.courses.find(course => 
      course.day === day && course.startTime === startTime
    ) || null;
  }

  isCurrentTime(day: string, startTime: string): boolean {
    const now = new Date();
    const today = now.toLocaleDateString('fr-FR', { weekday: 'long' });
    const currentTime = now.getHours() * 60 + now.getMinutes();
    const [hours, minutes] = startTime.split(':').map(Number);
    const slotTime = hours * 60 + minutes;
    
    return today.toLowerCase() === day.toLowerCase() && 
           Math.abs(currentTime - slotTime) < 90; // Within 1.5 hours
  }

  onWeekChange(): void {
    // Load data for selected week
    console.log('Week changed to:', this.selectedWeek);
  }

  onSubjectChange(): void {
    // Filter courses by subject
    console.log('Subject filter changed to:', this.selectedSubject);
  }

  viewCourseDetails(course: Course): void {
    console.log('View course details:', course);
    // Navigate to course details or open modal
  }

  markAbsence(course: Course, event: Event): void {
    event.stopPropagation();
    console.log('Mark absence for course:', course);
    // Navigate to absence reporting
  }

  scheduleMapping(course: Course, event: Event): void {
    event.stopPropagation();
    console.log('Schedule makeup for course:', course);
    // Navigate to makeup scheduling
  }

  exportTimetable(): void {
    console.log('Export timetable');
    // Implementation for export functionality
  }

  printTimetable(): void {
    console.log('Print timetable');
    window.print();
  }

  private calculateWeeklyStats(): void {
    this.weeklyStats = {
      totalHours: this.courses.length * 1.5, // Assuming 1.5 hours per course
      totalCourses: this.courses.length,
      uniqueGroups: new Set(this.courses.map(c => c.group)).size
    };
  }
}
