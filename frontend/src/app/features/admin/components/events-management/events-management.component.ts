import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { EventsClient } from '../../../../core/services/events.service';

interface EvItem { id: number; titre: string; date: string; description?: string; type?: string }

@Component({
  selector: 'app-events-management',
  standalone: true,
  imports: [CommonModule, FormsModule, MatButtonModule, MatInputModule, MatIconModule],
  templateUrl: './events-management.component.html',
  styleUrls: ['./events-management.component.css']
})
export class EventsManagementComponent implements OnInit {
  events: EvItem[] = [];
  loading = false;
  showForm = false;
  form: Partial<EvItem & { type?: string }> = { titre: '', date: '', description: '' };
  editingId: number | null = null;
  // available event types for admin selection
  eventTypes = [
    { value: 'default', label: 'Par défaut' },
    { value: 'institutionnel', label: 'Institutionnel' },
    { value: 'conference', label: 'Conférence' },
    { value: 'hackathon', label: 'Hackathon' },
  ];

  constructor(private eventsClient: EventsClient) {}

  ngOnInit(): void {
    this.load();
  }

  load() {
    this.loading = true;
    this.eventsClient.listEvents().subscribe({
      next: list => {
        this.events = list.map(e => ({ id: e.id, titre: e.titre, date: (e.date || '').slice(0,10), description: e.description || '', type: e.type || '' }));
        this.loading = false;
      },
      error: err => { console.error(err); this.loading = false; }
    });
  }

  toggleForm() { this.showForm = !this.showForm; }

  submit() {
    if (!this.form.titre || !this.form.date) return;
    const isoDate = this.form.date!.includes('T') ? this.form.date! : `${this.form.date}T09:00:00`;
    const payload = { titre: this.form.titre!, type: this.form.type || 'institutionnel', date: isoDate, description: this.form.description || '' };
    if (this.editingId) {
      this.eventsClient.updateEvent(this.editingId, payload).subscribe({ next: ev => { this.load(); this.showForm = false; this.form = { titre: '', date: '', description: '' }; this.editingId = null; }, error: err => console.error('update failed', err) });
    } else {
      this.eventsClient.createEvent(payload).subscribe({ next: ev => { this.load(); this.showForm = false; this.form = { titre: '', date: '', description: '' }; }, error: err => console.error('create failed', err) });
    }
  }

  editEvent(ev: EvItem) {
    this.editingId = ev.id;
    this.form = { titre: ev.titre, date: ev.date, description: ev.description, type: ev.type };
    this.showForm = true;
    // focus could be added if desired
  }

  cancelEdit() {
    this.editingId = null;
    this.form = { titre: '', date: '', description: '' };
    this.showForm = false;
  }

  deleteEvent(ev: EvItem) {
    if (!confirm(`Supprimer l'événement « ${ev.titre} » ?`)) return;
    this.eventsClient.deleteEvent(ev.id).subscribe({ next: () => { this.load(); }, error: err => console.error('delete failed', err) });
  }
}
