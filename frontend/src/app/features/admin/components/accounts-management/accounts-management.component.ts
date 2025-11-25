import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../../core/services/api.service';
import { forkJoin } from 'rxjs';

interface AccountRow {
  id: string;
  avatar: string;
  name: string;
  job: string;
  email: string;
}

@Component({
  selector: 'admin-accounts-management',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './accounts-management.component.html',
  // reuse admin dashboard styles so the page keeps the exact same look
  styleUrls: ['../../pages/admin-dashboard/admin-dashboard.component.css', './accounts-management.component.css']
})
export class AccountsManagementComponent implements OnInit {
  // sample data adapted from your React example
  data: AccountRow[] = [
    {
      id: '1',
      avatar: 'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-1.png',
      name: 'Robert Wolfkisser',
      job: 'Engineer',
      email: 'rob_wolf@gmail.com'
    },
    {
      id: '2',
      avatar: 'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-7.png',
      name: 'Jill Jailbreaker',
      job: 'Engineer',
      email: 'jj@breaker.com'
    },
    {
      id: '3',
      avatar: 'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-2.png',
      name: 'Henry Silkeater',
      job: 'Designer',
      email: 'henry@silkeater.io'
    },
    {
      id: '4',
      avatar: 'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-3.png',
      name: 'Bill Horsefighter',
      job: 'Designer',
      email: 'bhorsefighter@gmail.com'
    },
    {
      id: '5',
      avatar: 'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-10.png',
      name: 'Jeremy Footviewer',
      job: 'Manager',
      email: 'jeremy@foot.dev'
    }
  ];

  // selection state (string ids)
  selection: string[] = ['1'];
  // search filter string
  filter = '';

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadAccounts();
  }

  get filteredData() {
    const q = this.filter?.trim().toLowerCase();
    if (!q) return this.data;
    return this.data.filter((d) => d.name.toLowerCase().includes(q) || d.email.toLowerCase().includes(q) || d.job.toLowerCase().includes(q));
  }

  // toggle a single row
  toggleRow(id: string) {
    const idx = this.selection.indexOf(id);
    if (idx > -1) this.selection = this.selection.filter((s) => s !== id);
    else this.selection = [...this.selection, id];
  }

  // toggle all visible rows
  toggleAll() {
    const allIds = this.data.map((d) => d.id);
    this.selection = this.selection.length === allIds.length ? [] : allIds;
  }

  // convenience getters used in template
  get allSelected() {
    return this.selection.length === this.data.length && this.data.length > 0;
  }

  get someSelected() {
    return this.selection.length > 0 && this.selection.length !== this.data.length;
  }

  // example bulk actions (placeholders)
  approveSelected() {
    if (this.selection.length === 0) return;
    const calls = this.selection.map(id => this.api.put(`/auth/admin/${id}/approve`, {}));
    forkJoin(calls).subscribe({ next: res => { console.log('approved', res); this.loadAccounts(); this.selection = []; }, error: err => { console.error('approve error', err); } });
  }

  rejectSelected() {
    if (this.selection.length === 0) return;
    const calls = this.selection.map(id => this.api.put(`/auth/admin/${id}/reject`, {}));
    forkJoin(calls).subscribe({ next: res => { console.log('rejected', res); this.loadAccounts(); this.selection = []; }, error: err => { console.error('reject error', err); } });
  }

  loadAccounts() {
    this.api.get<any[]>('/auth/admin/users').subscribe({ next: list => {
      this.data = list.map(u => ({ id: String(u.id), avatar: '', name: u.full_name || u.username, job: u.role || '', email: u.email }));
      // preserve valid selections
      this.selection = this.selection.filter(s => this.data.some(d => d.id === s));
    }, error: err => console.error('Failed loading accounts', err) });
  }
}
