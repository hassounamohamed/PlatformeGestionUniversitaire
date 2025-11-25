import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { LoginRequest } from '../../../models/user.model';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  showPassword = false;
  isLoading = false;
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });

    // Show a friendly message if redirected after registration and pending approval
    this.route.queryParams.subscribe(params => {
      if (params['pending'] === 'true') {
        this.errorMessage = 'Votre compte est créé et en attente de validation par un administrateur.';
      } else if (params['registered'] === 'true') {
        this.errorMessage = 'Inscription réussie. Vous pourrez vous connecter une fois le compte activé.';
      }
    });
  }

  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      this.isLoading = true;
      this.errorMessage = '';

      const credentials: LoginRequest = {
        email: this.loginForm.value.email,
        password: this.loginForm.value.password
      };

      this.authService.login(credentials).subscribe({
        next: (response) => {
          // La redirection est gérée automatiquement par le service selon le rôle
          this.isLoading = false;
        },
        error: (error) => {
          // Backend returns error detail in `detail` (FastAPI) or `message` in other cases
          // If backend returns 403 for pending approval, show a clear message
          if (error.status === 403) {
            this.errorMessage = 'Votre compte est en attente d\'approbation par un administrateur.';
          } else {
            this.errorMessage = error.error?.detail || error.error?.message || 'Invalid email or password';
          }
          this.isLoading = false;
        }
      });
    } else {
      this.markFormGroupTouched(this.loginForm);
    }
  }

  private markFormGroupTouched(formGroup: FormGroup): void {
    Object.keys(formGroup.controls).forEach(key => {
      const control = formGroup.get(key);
      control?.markAsTouched();
    });
  }

  goToRegister(): void {
    this.router.navigate(['/auth/register']);
  }
}