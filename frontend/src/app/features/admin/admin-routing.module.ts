import { Routes } from '@angular/router';
import { AdminDashboardComponent } from './pages/admin-dashboard/admin-dashboard.component';
import { GlobalReferentialsComponent } from './components/global-referentials/global-referentials.component';
import { EventsManagementComponent } from './components/events-management/events-management.component';
import { ReportsComponent } from './components/reports/reports.component';
import { TimetablesManagementComponent } from './components/timetables-management/timetables-management.component';
import { ConflictsManagementComponent } from './components/conflicts-management/conflicts-management.component';
import { AccountsManagementComponent } from './components/accounts-management/accounts-management.component';

export const adminRoutes: Routes = [
  {
    path: '',
    component: AdminDashboardComponent
  },
  {
    path: 'referentials',
    component: GlobalReferentialsComponent
  },
  {
    path: 'events',
    component: EventsManagementComponent
  },
  {
    path: 'reports',
    component: ReportsComponent
  },
  {
    path: 'timetables',
    component: TimetablesManagementComponent
  },
  {
    path: 'conflicts',
    component: ConflictsManagementComponent
  },
  {
    path: 'accounts',
    component: AccountsManagementComponent
  },
  {
    path: 'settings',
    component: AdminDashboardComponent
  }
];
