import { Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { ApiService } from '../../../core/services/api.service';

@Injectable({ providedIn: 'root' })
export class AdminService {
  constructor(private api: ApiService) {}

  private mapResourceToPath(resource: string): string {
    switch (resource) {
      case 'departments':
        return '/departements';
      case 'teachers':
        return '/enseignants';
      case 'specialties':
        return '/specialites';
      case 'students':
        return '/etudiants';
      case 'rooms':
        return '/salles';
      case 'subjects':
        return '/matieres';
      case 'events':
        return '/events';
      case 'emplois':
        return '/emplois';
      case 'analytics':
        return '/analytics';
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
}
