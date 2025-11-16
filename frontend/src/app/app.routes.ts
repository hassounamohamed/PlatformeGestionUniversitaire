import { Routes } from '@angular/router';

export const routes: Routes = [
	{ path: '', loadComponent: () => import('./components/landing/landing.component').then(m => m.LandingComponent) },

	// Auth routes - lazy-load standalone components
	{
		path: 'auth',
		children: [
			{ path: '', redirectTo: 'login', pathMatch: 'full' },
			{ path: 'login', loadComponent: () => import('./core/auth/components/login/login.component').then(m => m.LoginComponent) },
			{ path: 'register', loadComponent: () => import('./core/auth/components/register/register.component').then(m => m.RegisterComponent) }
		]
	},

	// Feature areas (lazy-loaded modules or standalone dashboards)
	{
		path: 'student',
		children: [
			{ path: '', loadComponent: () => import('./features/student/pages/student-dashboard/student-dashboard.component').then(m => m.StudentDashboardComponent) },
			{ path: 'dashboard', loadComponent: () => import('./features/student/pages/student-dashboard/student-dashboard.component').then(m => m.StudentDashboardComponent) },
			{ path: 'timetable', loadComponent: () => import('./features/student/components/timetable/timetable.component').then(m => m.TimetableComponent) },
			{ path: 'absences', loadComponent: () => import('./features/student/components/absences/absences.component').then(m => m.AbsencesComponent) },
			{ path: 'messages', loadComponent: () => import('./features/student/components/messages/messages.component').then(m => m.MessagesComponent) },
			{ path: 'grades', loadComponent: () => import('./features/student/components/grades/grades.component').then(m => m.GradesComponent) },
			{ path: 'notifications', loadComponent: () => import('./features/student/components/notifications/notifications.component').then(m => m.NotificationsComponent) }
		]
	},
	{ 
		path: 'teacher',
		children: [
			{ path: '', loadComponent: () => import('./features/teacher/pages/teacher-dashboard/teacher-dashboard.component').then(m => m.TeacherDashboardComponent) },
			{ path: 'dashboard', loadComponent: () => import('./features/teacher/pages/teacher-dashboard/teacher-dashboard.component').then(m => m.TeacherDashboardComponent) },
			{ path: 'timetable', loadComponent: () => import('./features/teacher/components/timetable/timetable.component').then(m => m.TimetableComponent) },
			{ path: 'absences', loadComponent: () => import('./features/teacher/components/absences/absences.component').then(m => m.AbsencesComponent) },
			{ path: 'makeup', loadComponent: () => import('./features/teacher/components/makeup/makeup.component').then(m => m.MakeupComponent) },
			{ path: 'messages', loadComponent: () => import('./features/teacher/components/messages/messages.component').then(m => m.MessagesComponent) }
		]
	},
	{ 
		path: 'director',
		children: [
			{ path: '', loadComponent: () => import('./features/director/pages/director-dashboard/director-dashboard.component').then(m => m.DirectorDashboardComponent) },
			{ path: 'dashboard', loadComponent: () => import('./features/director/pages/director-dashboard/director-dashboard.component').then(m => m.DirectorDashboardComponent) },
			{ path: 'timetable', loadComponent: () => import('./features/director/pages/timetable-page/timetable-page.component').then(m => m.TimetablePageComponent) },
			{ path: 'timetable/create', loadComponent: () => import('./features/director/components/timetable-creator/timetable-creator.component').then(m => m.TimetableCreatorComponent) },
			{ path: 'stats', loadComponent: () => import('./features/director/pages/stats-page/stats-page.component').then(m => m.StatsPageComponent) },
			{ path: 'subjects', loadComponent: () => import('./features/director/pages/referentials-page/referentials-page.component').then(m => m.ReferentialsPageComponent) },
			{ path: 'groups', loadComponent: () => import('./features/director/pages/referentials-page/referentials-page.component').then(m => m.ReferentialsPageComponent) },
			{ path: 'makeup', loadComponent: () => import('./features/director/pages/makeup-page/makeup-page.component').then(m => m.MakeupPageComponent) },
			{ path: 'conflicts', loadComponent: () => import('./features/director/pages/conflicts-page/conflicts-page.component').then(m => m.ConflictsPageComponent) }
		]
	},
	{ 
		path: 'admin',
		children: [
			{ path: '', loadComponent: () => import('./features/admin/pages/admin-dashboard/admin-dashboard.component').then(m => m.AdminDashboardComponent) },
			{ path: 'dashboard', loadComponent: () => import('./features/admin/pages/admin-dashboard/admin-dashboard.component').then(m => m.AdminDashboardComponent) },
			{ path: 'referentials', loadComponent: () => import('./features/admin/components/global-referentials/global-referentials.component').then(m => m.GlobalReferentialsComponent) },
			{ path: 'events', loadComponent: () => import('./features/admin/components/events-management/events-management.component').then(m => m.EventsManagementComponent) },
			{ path: 'reports', loadComponent: () => import('./features/admin/components/reports/reports.component').then(m => m.ReportsComponent) },
			{ path: 'timetables', loadComponent: () => import('./features/admin/components/timetables-management/timetables-management.component').then(m => m.TimetablesManagementComponent) },
			{ path: 'conflicts', loadComponent: () => import('./features/admin/components/conflicts-management/conflicts-management.component').then(m => m.ConflictsManagementComponent) },
			{ path: 'settings', loadComponent: () => import('./features/admin/pages/admin-dashboard/admin-dashboard.component').then(m => m.AdminDashboardComponent) },
			{path: 'accounts', loadComponent: () => import('./features/admin/components/accounts-management/accounts-management.component').then(m => m.AccountsManagementComponent) }
		]
  	},

	{ path: '**', loadComponent: () => import('./components/not-found/not-found.component').then(m => m.NotFoundComponent) }
];
