import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, tap } from 'rxjs';
import { Router } from '@angular/router';
import { User, UserRole, LoginRequest, RegisterRequest, AuthResponse } from '../../models/user.model';
import { BASE_API } from '../../../app.api';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  // Point to the auth endpoint via centralized base. Use '/api' so proxy can forward to backend.
  private readonly API_URL = `${BASE_API}/auth`;
  private readonly TOKEN_KEY = 'auth_token';
  private readonly USER_KEY = 'current_user';

  private currentUserSubject = new BehaviorSubject<User | null>(this.getUserFromStorage());
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(
    private http: HttpClient,
    private router: Router
  ) {}

  /**
   * Connexion de l'utilisateur (sans sélection de rôle)
   * Le rôle est récupéré depuis la base de données
   */
  login(credentials: LoginRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.API_URL}/login`, credentials)
      .pipe(
        tap(response => {
          // Backend returns access_token and user
          const token = (response as any).access_token || (response as any).token;
          const user = (response as any).user;
          console.debug('AuthService.login response', { token, user });
          if (token && user) {
            // Normalize role and store
            const normalizedUser = { ...user, role: this.normalizeRole(user.role) } as any;
            this.setSession({ access_token: token, user: normalizedUser } as any);
            this.currentUserSubject.next(normalizedUser);
            this.redirectByRole(normalizedUser.role);
          }
        }, err => {
          console.error('AuthService.login error', err);
        })
      );
  }

  /**
   * Inscription (optionnelle - peut être désactivée)
   * Si activée, l'utilisateur sera automatiquement créé avec le rôle "student"
   */
  register(data: RegisterRequest): Observable<any> {
    // Backend register endpoint returns the created user (UserResponse)
    return this.http.post<any>(`${this.API_URL}/register`, {
      ...data,
      // role: 'student' // backend may assign default role; uncomment if backend expects role
    });
  }

  /**
   * Déconnexion
   */
  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    this.currentUserSubject.next(null);
    this.router.navigate(['/auth/login']);
  }

  /**
   * Vérifie si l'utilisateur est authentifié
   */
  isAuthenticated(): boolean {
    const token = this.getToken();
    return !!token && !this.isTokenExpired(token);
  }

  /**
   * Récupère l'utilisateur actuel
   */
  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }

  /**
   * Récupère le token d'authentification
   */
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * Vérifie si l'utilisateur a un rôle spécifique
   */
  hasRole(role: UserRole): boolean {
    const user = this.getCurrentUser();
    return user?.role === role;
  }

  /**
   * Vérifie si l'utilisateur a l'un des rôles spécifiés
   */
  hasAnyRole(roles: UserRole[]): boolean {
    const user = this.getCurrentUser();
    return user ? roles.includes(user.role) : false;
  }

  /**
   * Stocke la session de l'utilisateur
   */
  private setSession(authResponse: any): void {
    const token = authResponse.access_token || authResponse.token;
    const user = authResponse.user;
    if (token) {
      localStorage.setItem(this.TOKEN_KEY, token);
    }
    if (user) {
      // Ensure stored user has a normalized role
      const u = { ...user, role: this.normalizeRole(user.role) };
      localStorage.setItem(this.USER_KEY, JSON.stringify(u));
    }
  }

  /**
   * Normalize backend role strings (French values) to frontend UserRole values
   */
  private normalizeRole(rawRole: string | undefined): any {
    if (!rawRole) return 'student';
    // Normalize common variants: replace spaces with underscore and lowercase
    const r = String(rawRole).toLowerCase().replace(/\s+/g, '_');
    switch (r) {
      case 'etudiant':
      case 'student':
        return 'student';
      case 'enseignant':
      case 'teacher':
        return 'teacher';
      case 'directeur':
      case 'director':
      case 'chef_de_departement':
      case 'chef_departement':
      case 'chef_de_dept':
      case 'chef':
        // Treat department head as director-level for routing purposes
        return 'director';
      case 'admin':
      case 'administrator':
        return 'admin';
      default:
        return 'student';
    }
  }

  /**
   * Récupère l'utilisateur depuis le localStorage
   */
  private getUserFromStorage(): User | null {
    const userJson = localStorage.getItem(this.USER_KEY);
    return userJson ? JSON.parse(userJson) : null;
  }

  /**
   * Vérifie si le token est expiré
   */
  private isTokenExpired(token: string): boolean {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const expiry = payload.exp * 1000; // Convert to milliseconds
      return Date.now() > expiry;
    } catch (error) {
      return true;
    }
  }

  /**
   * Redirige l'utilisateur selon son rôle
   */
  private redirectByRole(role: UserRole): void {
    const routes: Record<UserRole, string> = {
      student: '/student/dashboard',
      teacher: '/teacher/dashboard',
      admin: '/admin/dashboard',
      director: '/director/dashboard'
    };
    const target = routes[role as UserRole] || '/';
    try {
      this.router.navigate([target]);
    } catch (err) {
      console.error('redirectByRole failed', err, { role, target });
      this.router.navigate(['/']);
    }
  }
}
