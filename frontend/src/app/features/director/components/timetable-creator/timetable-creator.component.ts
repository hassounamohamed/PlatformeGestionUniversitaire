import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CdkDragDrop, DragDropModule, transferArrayItem } from '@angular/cdk/drag-drop';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { TimetableCreatorService } from './timetable-creator.service';
import { DirectorService } from '../../services/director.service';
import { HttpClient } from '@angular/common/http';

interface CourseItem {
  id: string;
  matiere_nom: string;
  enseignant_nom: string;
  groupe_nom: string;
  salle_numero: string;
}

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
    MatChipsModule,
    MatProgressSpinnerModule
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

  // Departement informatique groups
  groups = [
    'TI11', 'TI12', 'TI13', 'TI14', 'TI15', 'TI16', 'TI17', 'TI18',
    'DSI21', 'DSI22', 'DSI23', 'RSI21',
    'DSI31', 'DSI32', 'RSI31'
  ];

  // Data loaded from API
  matieres: any[] = [];
  enseignants: any[] = [];
  salles: any[] = [];
  groupesList: any[] = [];
  loading = false;

  // palette of courses to drag
  courses: CourseItem[] = [];

  // grid: dayIndex x timeIndex -> array of scheduled items
  grid: Array<Array<CourseItem[]>> = [];

  // Connected drop list IDs
  paletteListId = 'palette-list';
  gridListIds: string[][] = [];

  courseForm!: FormGroup;

  constructor(
    private creatorService: TimetableCreatorService,
    private directorService: DirectorService,
    private http: HttpClient,
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    this.initGrid();
    this.courseForm = this.fb.group({
      matiere_nom: ['', Validators.required],
      enseignant_nom: ['', Validators.required],
      groupe_nom: ['', Validators.required],
      salle_numero: ['', Validators.required]
    });
    this.loadReferenceData();
  }

  loadReferenceData() {
    this.loading = true;
    const referentielBase = 'http://127.0.0.1:8003';
    
    // Load matieres
    this.http.get<any[]>(`${referentielBase}/matieres/`).subscribe({
      next: (data) => {
        this.matieres = data.sort((a, b) => a.nom.localeCompare(b.nom));
        console.log('Matières chargées:', this.matieres.length);
      },
      error: (err) => console.error('Erreur chargement matières:', err)
    });

    // Load enseignants
    this.http.get<any[]>(`${referentielBase}/enseignants/`).subscribe({
      next: (data) => {
        this.enseignants = data.map(e => ({
          ...e,
          full_name: `${e.prenom} ${e.nom}`
        })).sort((a, b) => a.full_name.localeCompare(b.full_name));
        console.log('Enseignants chargés:', this.enseignants.length);
      },
      error: (err) => console.error('Erreur chargement enseignants:', err)
    });

    // Load groupes (from referentiel service) - contains id and nom
    this.http.get<any[]>(`${referentielBase}/groupes/`).subscribe({
      next: (data) => {
        // keep full objects so we can send groupe_id when saving
        this.groupesList = data;
        this.groups = data.map(g => g.nom);
        console.log('Groupes chargés:', data.length);
      },
      error: (err) => console.error('Erreur chargement groupes:', err)
    });

    // Load salles
    this.http.get<any[]>(`${referentielBase}/salles/`).subscribe({
      next: (data) => {
        // API returns `code` for the salle identifier; map to `numero` used by the UI
        this.salles = data
          .map(s => ({ ...s, numero: s.code }))
          .sort((a, b) => (a.numero || '').localeCompare(b.numero || ''));
        console.log('Salles chargées:', this.salles.length);
        this.loading = false;
      },
      error: (err) => {
        console.error('Erreur chargement salles:', err);
        this.loading = false;
      }
    });
  }

  initGrid() {
    this.grid = [];
    this.gridListIds = [];
    for (let d = 0; d < this.daysOfWeek.length; d++) {
      const col: Array<CourseItem[]> = [];
      const idCol: string[] = [];
      for (let t = 0; t < this.timeSlots.length; t++) {
        col.push([]);
        idCol.push(`cell-${d}-${t}`);
      }
      this.grid.push(col);
      this.gridListIds.push(idCol);
    }
  }

  addCourse() {
    if (this.courseForm.invalid) return;
    const val = this.courseForm.value;
    const id = `c-${Date.now()}`;
    this.courses.push({
      id,
      matiere_nom: val.matiere_nom,
      enseignant_nom: val.enseignant_nom,
      groupe_nom: val.groupe_nom,
      salle_numero: val.salle_numero
    });
    this.courseForm.reset();
  }

  drop(event: CdkDragDrop<CourseItem[]>) {
    if (event.previousContainer === event.container) {
      // Same container - no action needed for now
      return;
    }
    // Transfer item from previous container to new container
    transferArrayItem(
      event.previousContainer.data,
      event.container.data,
      event.previousIndex,
      event.currentIndex
    );
  }

  removeFromCell(day: number, time: number, index: number) {
    const item = this.grid[day][time][index];
    this.grid[day][time].splice(index, 1);
    // Return to palette
    this.courses.push(item);
  }

  getConnectedLists(): string[] {
    const all = [this.paletteListId];
    for (let d = 0; d < this.gridListIds.length; d++) {
      for (let t = 0; t < this.gridListIds[d].length; t++) {
        all.push(this.gridListIds[d][t]);
      }
    }
    return all;
  }

  saveTimetable() {
    // Convert grid to EmploiTempsCreate payloads
    const payload: any[] = [];
    // Get current Monday as base date
    const today = new Date();
    const dayOfWeek = today.getDay();
    const diff = dayOfWeek === 0 ? -6 : 1 - dayOfWeek; // Monday as week start
    const baseDate = new Date(today);
    baseDate.setDate(today.getDate() + diff);

    for (let d = 0; d < this.grid.length; d++) {
      for (let t = 0; t < this.grid[d].length; t++) {
        const items = this.grid[d][t];
        items.forEach((course: CourseItem) => {
          const dayDate = new Date(baseDate);
          dayDate.setDate(baseDate.getDate() + d);
          const dateStr = dayDate.toISOString().split('T')[0];

          const [startTime, endTime] = this.timeSlots[t].split('-');
          // Resolve ids from loaded reference data
          const matiereObj = this.matieres.find(m => m.nom === course.matiere_nom) || null;
          const enseignantObj = this.enseignants.find(e => e.full_name === course.enseignant_nom || (`${e.prenom} ${e.nom}`) === course.enseignant_nom || (`${e.nom} ${e.prenom}`) === course.enseignant_nom) || null;
          // groups list may be simple strings or fetched objects; try to resolve by name
          const groupeObjName = course.groupe_nom;
          const groupeObj = this.groupesList.find(g => g.nom === groupeObjName) || null;
          // we may not have group ids in this component; attempt to fetch mapping from referentiel if available
          // For now assume group names correspond to API groupe noms and will be resolved server-side if needed
          const salleObj = this.salles.find(s => (s.numero || s.code) === course.salle_numero || s.code === course.salle_numero) || null;

          payload.push({
            date: dateStr,
            heure_debut: startTime,
            heure_fin: endTime,
            salle_id: salleObj ? salleObj.id : (parseInt(course.salle_numero, 10) || 1),
            matiere_id: matiereObj ? matiereObj.id : undefined,
            enseignant_id: enseignantObj ? enseignantObj.id : undefined,
            groupe_nom: groupeObjName,
            groupe_id: groupeObj ? groupeObj.id : undefined,
            matiere_nom: course.matiere_nom,
            enseignant_nom: course.enseignant_nom
          });
        });
      }
    }

    if (payload.length === 0) {
      alert('Aucun cours placé dans la grille.');
      return;
    }

    // Send to backend emploi_service
    // include trailing slash to avoid redirect which can complicate CORS preflight
    const url = 'http://127.0.0.1:8004/emplois/';
    let successCount = 0;
    let errorCount = 0;

    payload.forEach((emp, idx) => {
      this.http.post(url, emp).subscribe({
        next: (res) => {
          successCount++;
          if (successCount + errorCount === payload.length) {
            alert(`Emploi du temps sauvegardé: ${successCount} créneaux créés, ${errorCount} erreurs.`);
          }
        },
        error: (err) => {
          console.error('Error creating emploi', err);
          errorCount++;
          if (successCount + errorCount === payload.length) {
            alert(`Emploi du temps sauvegardé: ${successCount} créneaux créés, ${errorCount} erreurs.`);
          }
        }
      });
    });
  }
}
