import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class TimetableCreatorService {
  private initialGroups: any[] = [];
  private createdTimetable = new BehaviorSubject<any[] | null>(null);

  setInitialGroups(groups: any[]) {
    this.initialGroups = groups || [];
  }

  getInitialGroups(): any[] {
    return this.initialGroups;
  }

  setCreatedTimetable(payload: any[]) {
    this.createdTimetable.next(payload);
  }

  getCreatedTimetable$() {
    return this.createdTimetable.asObservable();
  }
}
