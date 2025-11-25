import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { FormBuilder, FormGroup, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { RegisterRequest } from '../../../models/user.model';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  showPassword = false;
  showConfirmPassword = false;
  isLoading = false;
  errorMessage = '';

  // OPTION: Pour désactiver complètement l'inscription publique,
  // vous pouvez masquer cette route ou rediriger vers login
  
  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    // OPTION: Pour désactiver l'inscription, décommentez la ligne suivante
    // this.router.navigate(['/auth/login']);
    
    this.registerForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(50)]],
      role: ['etudiant', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6), this.passwordStrengthValidator]],
      confirmPassword: ['', [Validators.required]],
      // Make the agreement checkbox optional so registration can proceed
      agree: [false]
    }, {
      validators: this.passwordMatchValidator
    });
  }

  // Custom validator for password strength
  passwordStrengthValidator(control: AbstractControl): ValidationErrors | null {
    const value = control.value;
    if (!value) {
      return null;
    }

    const hasNumber = /[0-9]/.test(value);
    const hasUpper = /[A-Z]/.test(value);
    const hasLower = /[a-z]/.test(value);

    const passwordValid = hasNumber && hasUpper && hasLower;

    return !passwordValid ? { passwordStrength: true } : null;
  }

  // Custom validator for password match
  passwordMatchValidator(form: AbstractControl): ValidationErrors | null {
    const password = form.get('password');
    const confirmPassword = form.get('confirmPassword');

    if (!password || !confirmPassword) {
      return null;
    }

    return password.value === confirmPassword.value ? null : { passwordMismatch: true };
  }

  togglePasswordVisibility(field: 'password' | 'confirmPassword'): void {
    if (field === 'password') {
      this.showPassword = !this.showPassword;
    } else {
      this.showConfirmPassword = !this.showConfirmPassword;
    }
  }

  onSubmit(): void {
    if (this.registerForm.valid) {
      this.isLoading = true;
      this.errorMessage = '';

      const registerData: RegisterRequest = {
        full_name: this.registerForm.value.name,
        email: this.registerForm.value.email,
        password: this.registerForm.value.password,
        role: this.registerForm.value.role,
        // Provide username: try explicit form value, else derive from email local-part
        username: this.registerForm.value['username'] || (this.registerForm.value.email || '').split('@')[0]
      };

      this.authService.register(registerData).subscribe({
        next: (response) => {
          // Succès - montrer message d'attente d'approbation
          // Redirect to login with a flag so login page can show info
          this.router.navigate(['/auth/login'], {
            queryParams: { registered: 'true', pending: 'true' }
          });
          this.isLoading = false;
        },
        error: (error) => {
          this.errorMessage = error.error?.detail || error.error?.message || 'Registration failed. Please try again.';
          this.isLoading = false;
        }
      });
    } else {
      this.markFormGroupTouched(this.registerForm);
    }
  }

  private markFormGroupTouched(formGroup: FormGroup): void {
    Object.keys(formGroup.controls).forEach(key => {
      const control = formGroup.get(key);
      control?.markAsTouched();
    });
  }

  goToLogin(): void {
    this.router.navigate(['/auth/login']);
  }

  getPasswordStrength(): string {
    const password = this.registerForm.get('password')?.value || '';
    if (password.length === 0) return '';
    if (password.length < 6) return 'weak';
    
    const hasNumber = /[0-9]/.test(password);
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    const strength = [hasNumber, hasUpper, hasLower, hasSpecial].filter(Boolean).length;
    
    if (strength <= 2) return 'weak';
    if (strength === 3) return 'medium';
    return 'strong';
  }
}