import { Routes } from '@angular/router';
import { DirectorDashboardComponent } from './pages/director-dashboard/director-dashboard.component';
import { TimetablePageComponent } from './pages/timetable-page/timetable-page.component';
import { StatsPageComponent } from './pages/stats-page/stats-page.component';
import { ReferentialsPageComponent } from './pages/referentials-page/referentials-page.component';
import { MakeupPageComponent } from './pages/makeup-page/makeup-page.component';
import { ConflictsPageComponent } from './pages/conflicts-page/conflicts-page.component';
import { TimetableCreatorComponent } from './components/timetable-creator/timetable-creator.component';

export const directorRoutes: Routes = [
  {
    path: '',
    component: DirectorDashboardComponent
  },
  {
    path: 'dashboard',
    component: DirectorDashboardComponent
  },
  {
    path: 'timetable',
    component: TimetablePageComponent
  },
  {
    path: 'timetable/create',
    component: TimetableCreatorComponent
  },
  {
    path: 'stats',
    component: StatsPageComponent
  },
  {
    path: 'subjects',
    component: ReferentialsPageComponent
  },
  {
    path: 'groups/create',
    component: ReferentialsPageComponent
  },
  {
    path: 'groups',
    component: ReferentialsPageComponent
  },
  {
    path: 'makeup',
    component: MakeupPageComponent
  },
  {
    path: 'conflicts',
    component: ConflictsPageComponent
  }
];
