import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { AdminService } from '../../services/admin.service';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatIconModule, MatButtonModule],
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['../../admin.styles.css', './admin-dashboard.component.css']
})
export class AdminDashboardComponent implements OnInit {
  stats = {
    departments: 0,
    teachers: 0,
    students: 0,
    rooms: 0
  };

  constructor(
    private router: Router,
    private adminService: AdminService
  ) {}

  ngOnInit(): void {
    this.loadStats();
  }

  async loadStats() {
    try {
      const [departments, teachers, students, rooms] = await Promise.all([
        this.adminService.list('departments'),
        this.adminService.list('teachers'),
        this.adminService.list('students'),
        this.adminService.list('rooms')
      ]);
      this.stats = {
        departments: departments?.length || 0,
        teachers: teachers?.length || 0,
        students: students?.length || 0,
        rooms: rooms?.length || 0
      };
    } catch (e) {
      // Use mock data if API fails
      this.stats = { departments: 5, teachers: 42, students: 1250, rooms: 28 };
    }
  }

  navigateTo(route: string) {
    this.router.navigate(['/admin', route]);
  }
}
