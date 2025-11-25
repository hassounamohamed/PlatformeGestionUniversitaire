export type UserRole = 'student' | 'teacher' | 'admin' | 'director';

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  createdAt?: Date;
  updatedAt?: Date;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  // Optionnel: le rôle demandé à l'inscription. Par défaut 'etudiant'.
  role?: 'etudiant' | 'enseignant';
  // Optional username to satisfy backend schema; if omitted frontend will send a derived value
  username?: string;
}

export interface AuthResponse {
  user: User;
  // Backend returns access_token (JWT) and token_type
  access_token: string;
  token_type?: string;
}
