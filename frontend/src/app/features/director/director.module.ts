import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

// Material Modules
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule } from '@angular/material/dialog';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatMenuModule } from '@angular/material/menu';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

// Routes
import { directorRoutes } from './director-routing.module';

// Components
import { DirectorDashboardComponent } from './pages/director-dashboard/director-dashboard.component';
import { TimetableManagementComponent } from './components/timetable-management/timetable-management.component';
import { TimetableCreatorComponent } from './components/timetable-creator/timetable-creator.component';
import { DepartmentStatsComponent } from './components/department-stats/department-stats.component';
import { ReferentialsComponent } from './components/referentials/referentials.component';

// Pages
import { TimetablePageComponent } from './pages/timetable-page/timetable-page.component';
import { StatsPageComponent } from './pages/stats-page/stats-page.component';
import { ReferentialsPageComponent } from './pages/referentials-page/referentials-page.component';
import { MakeupPageComponent } from './pages/makeup-page/makeup-page.component';
import { ConflictsPageComponent } from './pages/conflicts-page/conflicts-page.component';

// Services
import { DirectorService } from './services/director.service';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    HttpClientModule,
    RouterModule.forChild(directorRoutes),
    
    // Material Modules
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTableModule,
    MatTabsModule,
    MatDialogModule,
    MatSnackBarModule,
    MatMenuModule,
    MatChipsModule,
    MatProgressSpinnerModule,
    MatProgressBarModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
  DragDropModule,
  FormsModule,
  ReactiveFormsModule,
  // All components are standalone, so we import them here
    DirectorDashboardComponent,
    TimetableManagementComponent,
    TimetableCreatorComponent,
    DepartmentStatsComponent,
    ReferentialsComponent,
    TimetablePageComponent,
    StatsPageComponent,
    ReferentialsPageComponent,
    MakeupPageComponent,
    ConflictsPageComponent
  ],
  providers: [
    DirectorService
  ]
})
export class DirectorModule {}
