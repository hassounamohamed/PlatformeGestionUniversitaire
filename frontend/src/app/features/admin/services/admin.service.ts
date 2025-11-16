import { Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { ApiService } from '../../../core/services/api.service';

@Injectable({ providedIn: 'root' })
export class AdminService {
  constructor(private api: ApiService) {}

  private mapResourceToPath(resource: string): string {
    switch (resource) {
      // When the API gateway is not running, call services directly by port.
      // Referentiel (departements, enseignants, etudiants, matieres, salles) runs on 8001
      case 'departments':
        return 'http://127.0.0.1:8001/departements';
      case 'teachers':
        return 'http://127.0.0.1:8001/enseignants';
      case 'specialties':
        return 'http://127.0.0.1:8001/specialites';
      case 'students':
        return 'http://127.0.0.1:8001/etudiants';
      case 'rooms':
        return 'http://127.0.0.1:8001/salles';
      case 'subjects':
        return 'http://127.0.0.1:8001/matieres';
      // Events run on 8006
      case 'events':
        return 'http://127.0.0.1:8006/events';
      // Emploi (timetable) on 8002
      case 'emplois':
        return 'http://127.0.0.1:8002/emplois';
      // Analytics on 8005
      case 'analytics':
        return 'http://127.0.0.1:8005/analytics';
      default:
        // assume resource is already an API path
        return `/${resource}`;
    }
  }

  async list(resource: string): Promise<any[]> {
    const path = this.mapResourceToPath(resource);
    try {
      return await firstValueFrom(this.api.get<any[]>(path));
    } catch (e) {
      console.warn('AdminService.list failed', resource, e);
      return [];
    }
  }

  async get(resource: string, id: string): Promise<any | null> {
    const path = `${this.mapResourceToPath(resource)}/${id}`;
    try {
      return await firstValueFrom(this.api.get<any>(path));
    } catch (e) {
      return null;
    }
  }

  async create(resource: string, payload: any): Promise<any | null> {
    const path = this.mapResourceToPath(resource);
    try {
      return await firstValueFrom(this.api.post<any>(path, payload));
    } catch (e) {
      console.warn('AdminService.create failed', resource, e);
      return null;
    }
  }

  async update(resource: string, id: string, payload: any): Promise<any | null> {
    const path = `${this.mapResourceToPath(resource)}/${id}`;
    try {
      return await firstValueFrom(this.api.put<any>(path, payload));
    } catch (e) {
      console.warn('AdminService.update failed', resource, e);
      return null;
    }
  }

  async remove(resource: string, id?: string): Promise<void> {
    if (!id) return;
    const path = `${this.mapResourceToPath(resource)}/${id}`;
    try {
      await firstValueFrom(this.api.delete<void>(path));
    } catch (e) {
      console.warn('AdminService.remove failed', resource, e);
    }
  }

  /**
   * Register a new user in the auth service.
   * Used by the admin UI to create login credentials for referential entities (teachers/students).
   */
  async registerAuth(payload: any): Promise<any | null> {
    // Auth service routes are mounted under /api/auth in the auth_service
    const url = 'http://127.0.0.1:8000/api/auth/register';
    try {
      return await firstValueFrom(this.api.post<any>(url, payload));
    } catch (e) {
      console.warn('AdminService.registerAuth failed', e);
      return null;
    }
  }
}
