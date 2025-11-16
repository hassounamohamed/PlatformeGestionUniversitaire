import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CdkDragDrop, DragDropModule, transferArrayItem } from '@angular/cdk/drag-drop';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { TimetableCreatorService } from './timetable-creator.service';
import { DirectorService } from '../../services/director.service';

@Component({
  selector: 'app-timetable-creator',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    DragDropModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
    MatSelectModule,
    MatChipsModule
  ],
  templateUrl: './timetable-creator.component.html',
  styleUrls: ['./timetable-creator.component.css']
})
export class TimetableCreatorComponent implements OnInit {
  daysOfWeek = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
  timeSlots = [
    '08:30-10:00', '10:10-11:40', '11:50-13:20',
    '14:30-16:00', '16:10-17:40'
  ];

  // palette of subjects to drag
  subjects: Array<{ id: string; name: string; groupId?: string }> = [];

  // grid: dayIndex x timeIndex -> array of scheduled items
  grid: Array<Array<Array<any>>> = [];

  selectedGroupId: string | null = null;
  groups: any[] = [];

  constructor(
    private creatorService: TimetableCreatorService,
    private directorService: DirectorService
  ) {}

  ngOnInit(): void {
    this.initGrid();
    // load groups provided by the creator service if available or fetch
    const initial = this.creatorService.getInitialGroups();
    if (initial && initial.length) {
      this.groups = initial;
    } else {
      this.directorService.getGroups('dept-1').subscribe(g => this.groups = g);
    }
  }

  initGrid() {
    this.grid = [];
    for (let d = 0; d < this.daysOfWeek.length; d++) {
      const col: Array<Array<any>> = [];
      for (let t = 0; t < this.timeSlots.length; t++) {
        col.push([]);
      }
      this.grid.push(col);
    }
  }

  addSubject(name: string) {
    if (!name || !name.trim()) return;
    const id = `s-${Date.now()}`;
    this.subjects.push({ id, name: name.trim(), groupId: this.selectedGroupId || undefined });
  }

  drop(event: CdkDragDrop<any[]>, dayIndex?: number, timeIndex?: number) {
    // If dropped into a cell
    if (dayIndex !== undefined && timeIndex !== undefined) {
      const list = this.grid[dayIndex][timeIndex];
      // If dragging from palette
      if (event.previousContainer === event.container) {
        // reorder within cell
        return;
      }
      const item = event.previousContainer.data[event.previousIndex];
      // move item to cell
      transferArrayItem(event.previousContainer.data, list, event.previousIndex, event.currentIndex);
    } else {
      // drop back to palette
      transferArrayItem(event.previousContainer.data, event.container.data, event.previousIndex, event.currentIndex);
    }
  }

  removeFromCell(day: number, time: number, index: number) {
    this.grid[day][time].splice(index, 1);
  }

  saveTimetable() {
    // Gather scheduled items and send to creation service or API
    const payload: any[] = [];
    for (let d = 0; d < this.grid.length; d++) {
      for (let t = 0; t < this.grid[d].length; t++) {
        const items = this.grid[d][t];
        items.forEach((it: any) => {
          payload.push({
            subjectName: it.name,
            groupId: it.groupId,
            dayOfWeek: d,
            timeSlot: this.timeSlots[t]
          });
        });
      }
    }

    // Store in the service for now
    this.creatorService.setCreatedTimetable(payload);
    alert('Emploi du temps sauvegardé (local). Vous pouvez maintenant l\'exporter ou l\'envoyer au serveur.');
  }
}
