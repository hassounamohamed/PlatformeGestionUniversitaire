import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTooltipModule } from '@angular/material/tooltip';

interface TeacherStats {
  todayClasses: number;
  totalStudents: number;
  totalSubjects: number;
  pendingAbsences: number;
  makeupSessions: number;
  unreadMessages: number;
}

interface QuickAction {
  title: string;
  description: string;
  icon: string;
  route: string;
  color: string;
  badge?: number;
}

interface Course {
  id: string;
  subject: string;
  group: string;
  room: string;
  startTime: string;
  endTime: string;
}

interface Message {
  id: string;
  senderName: string;
  subject: string;
  date: Date;
  read: boolean;
}

@Component({
	selector: 'app-teacher-dashboard',
	standalone: true,
	imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatTooltipModule
  ],
	templateUrl: './teacher-dashboard.component.html',
	styleUrls: ['./teacher-dashboard.component.css']
})
export class TeacherDashboardComponent implements OnInit {
  loading = false;
  currentDate = new Date();

  stats: TeacherStats = {
    todayClasses: 4,
    totalStudents: 120,
    totalSubjects: 3,
    pendingAbsences: 5,
    makeupSessions: 2,
    unreadMessages: 8
  };

  quickActions: QuickAction[] = [
    {
      title: 'Emploi du Temps',
      description: 'Consultez votre planning de cours',
      icon: 'schedule',
      route: '/teacher/timetable',
      color: 'primary'
    },
    {
      title: 'Signaler Absence',
      description: 'Déclarez une absence avec motif',
      icon: 'person_off',
      route: '/teacher/absences',
      color: 'accent'
    },
    {
      title: 'Séances de Rattrapage',
      description: 'Proposez des sessions de rattrapage',
      icon: 'event_note',
      route: '/teacher/makeup',
      color: 'warn',
      badge: this.stats.makeupSessions
    },
    {
      title: 'Messagerie',
      description: 'Communiquez avec les étudiants',
      icon: 'mail',
      route: '/teacher/messages',
      color: 'primary',
      badge: this.stats.unreadMessages
    },
    {
      title: 'Validation Absences',
      description: 'Validez les demandes d\'absence',
      icon: 'check_circle',
      route: '/teacher/absences/validate',
      color: 'accent',
      badge: this.stats.pendingAbsences
    }
  ];

  todaySchedule: Course[] = [
    {
      id: '1',
      subject: 'Mathématiques Appliquées',
      group: 'L2 Info A',
      room: '101',
      startTime: '08:30',
      endTime: '10:00'
    },
    {
      id: '2',
      subject: 'Algorithmique',
      group: 'L1 Info B',
      room: '205',
      startTime: '10:10',
      endTime: '11:40'
    },
    {
      id: '3',
      subject: 'Base de Données',
      group: 'L2 Info A',
      room: '103',
      startTime: '14:30',
      endTime: '16:00'
    },
    {
      id: '4',
      subject: 'Programmation Web',
      group: 'L3 Info',
      room: '201',
      startTime: '16:10',
      endTime: '17:40'
    }
  ];

  recentMessages: Message[] = [
    {
      id: '1',
      senderName: 'Ahmed Ben Ali',
      subject: 'Demande de rattrapage',
      date: new Date('2025-10-10T14:30:00'),
      read: false
    },
    {
      id: '2',
      senderName: 'Fatma Gharbi',
      subject: 'Justificatif d\'absence',
      date: new Date('2025-10-10T11:15:00'),
      read: false
    },
    {
      id: '3',
      senderName: 'Mohamed Triki',
      subject: 'Question sur le cours',
      date: new Date('2025-10-09T16:45:00'),
      read: true
    }
  ];

  constructor(private router: Router) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.loading = true;
    // Simulation d'un appel API
    setTimeout(() => {
      this.loading = false;
    }, 1000);
  }

  navigateTo(route: string): void {
    this.router.navigate([route]);
  }

  markAbsence(course: Course): void {
    this.router.navigate(['/teacher/absences'], { 
      queryParams: { courseId: course.id } 
    });
  }
}
