import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface EventPayload {
  titre: string;
  type: string;
  date: string; // ISO datetime
  description?: string | null;
}

export interface BackendEvent extends EventPayload {
  id: number;
}

@Injectable({ providedIn: 'root' })
export class EventsClient {
  // Direct event service URL for local development
  private base = 'http://127.0.0.1:8006/events';
  // Notifies when events list should be refreshed (create/delete/update)
  private _eventsChanged = new Subject<void>();
  readonly eventsChanged$ = this._eventsChanged.asObservable();

  constructor(private http: HttpClient) {}

  listEvents(): Observable<BackendEvent[]> {
    return this.http.get<BackendEvent[]>(this.base);
  }

  createEvent(ev: EventPayload): Observable<BackendEvent> {
    return this.http.post<BackendEvent>(this.base, ev).pipe(
      tap(() => this._eventsChanged.next())
    );
  }

  getEvent(id: number) {
    return this.http.get<BackendEvent>(`${this.base}/${id}`);
  }

  updateEvent(id: number, ev: EventPayload) {
    return this.http.put<BackendEvent>(`${this.base}/${id}`, ev).pipe(
      tap(() => this._eventsChanged.next())
    );
  }

  deleteEvent(id: number) {
    return this.http.delete(`${this.base}/${id}`).pipe(
      tap(() => this._eventsChanged.next())
    );
  }
}
