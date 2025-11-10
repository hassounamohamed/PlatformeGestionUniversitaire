import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User, UserRole } from '../../../core/models/user.model';
import { BASE_API } from '../../../app.api';

export interface CreateUserRequest {
  name: string;
  email: string;
  password: string;
  role: UserRole;
}

export interface UpdateUserRequest {
  name?: string;
  email?: string;
  role?: UserRole;
  active?: boolean;
}

export interface UsersListResponse {
  users: User[];
  total: number;
  page: number;
  pageSize: number;
}

@Injectable({
  providedIn: 'root'
})
export class UserManagementService {
  private readonly API_URL = `${BASE_API}/admin/users`;

  constructor(private http: HttpClient) {}

  /**
   * Créer un nouveau utilisateur (tous rôles)
   * Réservé aux administrateurs
   */
  createUser(userData: CreateUserRequest): Observable<User> {
    return this.http.post<User>(this.API_URL, userData);
  }

  /**
   * Récupérer la liste des utilisateurs avec filtres optionnels
   */
  getUsers(filters?: {
    role?: UserRole;
    search?: string;
    page?: number;
    pageSize?: number;
  }): Observable<UsersListResponse> {
    let params = new HttpParams();
    
    if (filters?.role) {
      params = params.set('role', filters.role);
    }
    if (filters?.search) {
      params = params.set('search', filters.search);
    }
    if (filters?.page) {
      params = params.set('page', filters.page.toString());
    }
    if (filters?.pageSize) {
      params = params.set('pageSize', filters.pageSize.toString());
    }

    return this.http.get<UsersListResponse>(this.API_URL, { params });
  }

  /**
   * Récupérer un utilisateur par ID
   */
  getUserById(userId: string): Observable<User> {
    return this.http.get<User>(`${this.API_URL}/${userId}`);
  }

  /**
   * Mettre à jour un utilisateur
   */
  updateUser(userId: string, updates: UpdateUserRequest): Observable<User> {
    return this.http.patch<User>(`${this.API_URL}/${userId}`, updates);
  }

  /**
   * Modifier le rôle d'un utilisateur
   */
  updateUserRole(userId: string, role: UserRole): Observable<User> {
    return this.http.patch<User>(`${this.API_URL}/${userId}/role`, { role });
  }

  /**
   * Activer/Désactiver un compte utilisateur
   */
  toggleUserStatus(userId: string, active: boolean): Observable<User> {
    return this.http.patch<User>(`${this.API_URL}/${userId}/status`, { active });
  }

  /**
   * Supprimer un utilisateur
   */
  deleteUser(userId: string): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${userId}`);
  }

  /**
   * Réinitialiser le mot de passe d'un utilisateur
   */
  resetPassword(userId: string, newPassword: string): Observable<void> {
    return this.http.post<void>(`${this.API_URL}/${userId}/reset-password`, {
      password: newPassword
    });
  }

  /**
   * Générer un mot de passe temporaire pour un utilisateur
   */
  generateTemporaryPassword(userId: string): Observable<{ temporaryPassword: string }> {
    return this.http.post<{ temporaryPassword: string }>(
      `${this.API_URL}/${userId}/generate-password`,
      {}
    );
  }

  /**
   * Obtenir les statistiques des utilisateurs par rôle
   */
  getUsersStats(): Observable<Record<UserRole, number>> {
    return this.http.get<Record<UserRole, number>>(`${this.API_URL}/stats`);
  }
}
