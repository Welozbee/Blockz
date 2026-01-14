import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  imports: [CommonModule, FormsModule, MatCardModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  username = '';
  password = '';
  message = '';
  isLoading = false;
  isOpen = false;
  displayName = '';

  constructor(private authService: AuthService) {}

  open(): void {
    this.message = '';
    this.isOpen = true;
  }

  close(): void {
    this.isOpen = false;
  }

  setDefaultUsername(username: string | null): void {
    this.displayName = username ?? '';
  }

  onSubmit(): void {
    if (!this.username || !this.password) {
      this.message = 'Identifiants requis.';
      return;
    }

    this.isLoading = true;
    this.message = '';
    this.authService.login(this.username, this.password).subscribe({
      next: (res) => {
        this.displayName = this.username;
        this.message = '';
        this.isLoading = false;
        this.close();
      },
      error: () => {
        this.message = 'Identifiants invalides.';
        this.isLoading = false;
      }
    });
  }
}
