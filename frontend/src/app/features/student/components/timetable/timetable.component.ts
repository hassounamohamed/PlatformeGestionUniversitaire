import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';

interface Course {
  id: string;
  subject: string;
  teacher: string;
  room: string;
  type: 'lecture' | 'td' | 'tp';
  day: string;
  startTime: string;
  endTime: string;
}

@Component({
  selector: 'app-student-timetable',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule, MatIconModule, MatSelectModule, MatFormFieldModule],
  templateUrl: './timetable.component.html',
  styleUrls: ['./timetable.component.css']
})
export class TimetableComponent implements OnInit {
  selectedWeek = 'current';
  weeks = [
    { value: 'previous', label: 'Semaine pr\u00e9c\u00e9dente' },
    { value: 'current', label: 'Semaine actuelle' },
    { value: 'next', label: 'Semaine prochaine' }
  ];

  days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'];

  timeSlots = ['08:30', '10:10', '11:50', '14:30', '16:10'];

  courses: Course[] = [
    { id: 's1', subject: 'Programmation Web', teacher: 'Dr. Sami', room: '201', type: 'lecture', day: 'Lundi', startTime: '08:30', endTime: '10:00' },
    { id: 's2', subject: 'Base de Donn\u00e9es', teacher: 'Mme. Leila', room: '103', type: 'tp', day: 'Mardi', startTime: '14:30', endTime: '16:00' },
    { id: 's3', subject: 'Math\u00e9matiques Appliqu\u00e9es', teacher: 'Mr. Hassen', room: '101', type: 'td', day: 'Jeudi', startTime: '10:10', endTime: '11:40' }
  ];

  ngOnInit(): void {
    // could load student-specific timetable from API
  }

  getCourse(day: string, start: string): Course | null {
    return this.courses.find(c => c.day === day && c.startTime === start) || null;
  }

  requestExcuse(course: Course, event: Event): void {
    event.stopPropagation();
    console.log('Request excuse for', course);
  }
}
