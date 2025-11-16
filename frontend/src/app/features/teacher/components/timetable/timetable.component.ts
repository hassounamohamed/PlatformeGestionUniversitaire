import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatTooltipModule } from '@angular/material/tooltip';

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
  styleUrl: './timetable.component.css'
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

  courses: Course[] = [
    {
      id: '1',
      subject: 'Mathématiques Appliquées',
      group: 'L2 Info A',
      room: '101',
      type: 'lecture',
      day: 'Lundi',
      startTime: '08:30',
      endTime: '10:00'
    },
    {
      id: '2',
      subject: 'Algorithmique',
      group: 'L1 Info B',
      room: '205',
      type: 'td',
      day: 'Lundi',
      startTime: '10:10',
      endTime: '11:40'
    },
    {
      id: '3',
      subject: 'Base de Données',
      group: 'L2 Info A',
      room: '103',
      type: 'tp',
      day: 'Mardi',
      startTime: '14:30',
      endTime: '16:00'
    },
    {
      id: '4',
      subject: 'Programmation Web',
      group: 'L3 Info',
      room: '201',
      type: 'lecture',
      day: 'Mercredi',
      startTime: '08:30',
      endTime: '10:00'
    },
    {
      id: '5',
      subject: 'Mathématiques Appliquées',
      group: 'L2 Info B',
      room: '102',
      type: 'td',
      day: 'Jeudi',
      startTime: '10:10',
      endTime: '11:40'
    },
    {
      id: '6',
      subject: 'Algorithmique',
      group: 'L1 Info A',
      room: '204',
      type: 'tp',
      day: 'Vendredi',
      startTime: '16:10',
      endTime: '17:40'
    }
  ];

  weeklyStats: WeeklyStats = {
    totalHours: 12,
    totalCourses: 6,
    uniqueGroups: 4
  };

  upcomingMakeups: Makeup[] = [
    {
      subject: 'Base de Données',
      date: new Date('2025-10-19'),
      time: '14:30 - 16:00',
      room: '103'
    },
    {
      subject: 'Algorithmique',
      date: new Date('2025-10-20'),
      time: '10:10 - 11:40',
      room: '205'
    }
  ];

  ngOnInit(): void {
    this.calculateWeeklyStats();
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
