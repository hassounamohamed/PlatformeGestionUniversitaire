import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from '../../../core/services/api.service';

export interface AdminEvent {
  id: string;
  title: string;
  description?: string;
  date: string;
  location?: string;
}

@Injectable({ providedIn: 'root' })
export class EventsService {
  private path = '/events';

  constructor(private api: ApiService) {}

  listEvents(): Observable<AdminEvent[]> {
    return this.api.get<AdminEvent[]>(this.path);
  }

  getEvent(id: string): Observable<AdminEvent> {
    return this.api.get<AdminEvent>(`${this.path}/${id}`);
  }

  createEvent(event: Partial<AdminEvent>): Observable<AdminEvent> {
    return this.api.post<AdminEvent>(this.path, event);
  }

  updateEvent(id: string, event: Partial<AdminEvent>): Observable<AdminEvent> {
    return this.api.put<AdminEvent>(`${this.path}/${id}`, event);
  }

  deleteEvent(id: string): Observable<void> {
    return this.api.delete<void>(`${this.path}/${id}`);
  }
}
