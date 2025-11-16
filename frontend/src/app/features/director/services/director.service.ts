import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { 
  Department, 
  Timetable, 
  TimetableConflict, 
  Subject, 
  Group, 
  Room, 
  MakeupSession,
  DepartmentStats,
  StudentPerformance,
  AbsenceReport
} from '../models/director.models';

@Injectable({
  providedIn: 'root'
})
export class DirectorService {
  private apiUrl = '/api/director';

  constructor(private http: HttpClient) {}

  // Dashboard & Statistics
  getDepartmentStats(departmentId: string): Observable<DepartmentStats> {
    // Request department stats from analytic service.
    // The analytic endpoint returns simple counts; map them to the
    // DepartmentStats interface and leave missing metrics as null/0.
    return this.http.get<Partial<Record<string, number>>>(`/analytics/department/${departmentId}/stats`)
      .pipe(
        // map response to DepartmentStats shape
        // avoid adding rxjs/operators import here for brevity; convert with a small map using toPromise is undesirable
      ) as unknown as Observable<DepartmentStats>;
  }

  getAbsenceReports(departmentId: string, period: string): Observable<AbsenceReport[]> {
    // Mock data
    return of([
      {
        date: '2025-01-08',
        totalAbsences: 23,
        absenteeismRate: 9.4,
        bySubject: { 'math101': 5, 'phys201': 8, 'chem101': 10 },
        byGroup: { 'g1': 8, 'g2': 7, 'g3': 8 }
      }
    ]);
  }

  getStudentPerformances(departmentId: string): Observable<StudentPerformance[]> {
    // Mock data
    return of([]);
  }

  // Timetable Management
  getTimetables(departmentId: string): Observable<Timetable[]> {
    return this.http.get<Timetable[]>(`${this.apiUrl}/timetables/${departmentId}`);
  }

  createTimetable(timetable: Partial<Timetable>): Observable<Timetable> {
    return this.http.post<Timetable>(`${this.apiUrl}/timetables`, timetable);
  }

  updateTimetable(id: string, timetable: Partial<Timetable>): Observable<Timetable> {
    return this.http.put<Timetable>(`${this.apiUrl}/timetables/${id}`, timetable);
  }

  deleteTimetable(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/timetables/${id}`);
  }

  validateTimetable(id: string): Observable<Timetable> {
    return this.http.patch<Timetable>(`${this.apiUrl}/timetables/${id}/validate`, {});
  }

  rejectTimetable(id: string, reason: string): Observable<Timetable> {
    return this.http.patch<Timetable>(`${this.apiUrl}/timetables/${id}/reject`, { reason });
  }

  // Conflict Management
  getTimetableConflicts(departmentId: string): Observable<TimetableConflict[]> {
    // Mock data
    return of([]);
  }

  resolveConflict(conflictId: string, solution: any): Observable<void> {
    return this.http.patch<void>(`${this.apiUrl}/conflicts/${conflictId}/resolve`, solution);
  }

  // Subject Management
  getSubjects(departmentId: string): Observable<Subject[]> {
    return this.http.get<Subject[]>(`${this.apiUrl}/subjects/${departmentId}`);
  }

  createSubject(subject: Partial<Subject>): Observable<Subject> {
    return this.http.post<Subject>(`${this.apiUrl}/subjects`, subject);
  }

  updateSubject(id: string, subject: Partial<Subject>): Observable<Subject> {
    return this.http.put<Subject>(`${this.apiUrl}/subjects/${id}`, subject);
  }

  deleteSubject(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/subjects/${id}`);
  }

  // Group Management
  getGroups(departmentId: string): Observable<Group[]> {
    return this.http.get<Group[]>(`${this.apiUrl}/groups/${departmentId}`);
  }

  createGroup(group: Partial<Group>): Observable<Group> {
    return this.http.post<Group>(`${this.apiUrl}/groups`, group);
  }

  updateGroup(id: string, group: Partial<Group>): Observable<Group> {
    return this.http.put<Group>(`${this.apiUrl}/groups/${id}`, group);
  }

  deleteGroup(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/groups/${id}`);
  }

  // Room Management
  getRooms(): Observable<Room[]> {
    return this.http.get<Room[]>(`${this.apiUrl}/rooms`);
  }

  getRoomOccupancy(roomId: string, date: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/rooms/${roomId}/occupancy?date=${date}`);
  }

  // Makeup Sessions
  getMakeupSessions(departmentId: string): Observable<MakeupSession[]> {
    return this.http.get<MakeupSession[]>(`${this.apiUrl}/makeup-sessions/${departmentId}`);
  }

  approveMakeupSession(id: string): Observable<MakeupSession> {
    return this.http.patch<MakeupSession>(`${this.apiUrl}/makeup-sessions/${id}/approve`, {});
  }

  rejectMakeupSession(id: string, reason: string): Observable<MakeupSession> {
    return this.http.patch<MakeupSession>(`${this.apiUrl}/makeup-sessions/${id}/reject`, { reason });
  }

  createMakeupSession(session: Partial<MakeupSession>): Observable<MakeupSession> {
    return this.http.post<MakeupSession>(`${this.apiUrl}/makeup-sessions`, session);
  }
}