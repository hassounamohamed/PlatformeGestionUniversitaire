import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService } from '../../services/admin.service';

@Component({
  selector: 'admin-reports',
  standalone: true,
	imports: [CommonModule, FormsModule],
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.css']
})
export class ReportsComponent {
	reportTypes = [
		{ key: 'events', label: "Emplois du temps" },
		{ key: 'attendance', label: "Présences" },
		{ key: 'students', label: "Étudiants" },
		{ key: 'teachers', label: "Enseignants" }
	];
	selectedType = 'events';
	format: 'csv' | 'pdf' = 'csv';
	fromDate: string | null = null;
	toDate: string | null = null;
	department: string | null = null;
	loading = false;
	message: string | null = null;
	lastResult: any[] = [];

	// Suggestions pour le champ département / filière
	departments: string[] = [
		'Informatique', 'Mathématiques', 'Physique', 'Lettres', 'Économie', 'Droit', 'Biologie'
	];

	get formattedFrom(): string {
		if (!this.fromDate) return '';
		try { return new Date(this.fromDate).toLocaleDateString('fr-FR'); } catch { return this.fromDate; }
	}
	get formattedTo(): string {
		if (!this.toDate) return '';
		try { return new Date(this.toDate).toLocaleDateString('fr-FR'); } catch { return this.toDate; }
	}

	resetForm(){
		if (!confirm('Confirmer la réinitialisation du formulaire ? Cette action effacera vos filtres.')) return;
		this.fromDate = null;
		this.toDate = null;
		this.department = null;
		this.lastResult = [];
		this.message = null;
	}

	get selectedLabel(): string {
		const r = this.reportTypes.find(x => x.key === this.selectedType);
		return r ? r.label : '';
	}

	get previewHeaders(): string[] {
		return this.lastResult && this.lastResult.length ? Object.keys(this.lastResult[0]) : [];
	}

	constructor(private admin: AdminService) {}

	private downloadCSVFromArray(data: any[], filename = 'report.csv'){
		if (!data || !data.length) {
			this.message = 'Aucune donnée à exporter.';
			return;
		}
		const headers = Object.keys(data[0]);
		const rows = data.map(r => headers.map(h => (r[h] ?? '').toString()));
		const csv = [headers, ...rows].map(r => r.map(cell => '"'+String(cell).replace(/"/g,'""')+'"').join(',')).join('\n');
		const blob = new Blob([csv], { type: 'text/csv' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url; a.download = filename; a.click();
		URL.revokeObjectURL(url);
	}

	private printHTML(html: string){
		const w = window.open('', '_blank');
		if (!w) return;
		w.document.write(html);
		w.document.close();
		w.focus();
		w.print();
		w.close();
	}

	async generateReport(){
		this.message = null;
		this.loading = true;
		try{
			let data: any[] = [];
			// best-effort: use AdminService.list if available for common resources
			if (this.selectedType === 'events') {
				data = await this.admin.list('events');
			} else if (this.selectedType === 'students') {
				// attempt to fetch students; service may return [] if endpoint missing
				data = await this.admin.list('students');
			} else {
				// fallback mock
				data = [ { id: '1', name: 'Exemple', date: new Date().toISOString().slice(0,10) } ];
			}

			// basic client-side filtering by date if fields provided
			if (this.fromDate || this.toDate) {
				const from = this.fromDate ? new Date(this.fromDate).getTime() : -Infinity;
				const to = this.toDate ? new Date(this.toDate).getTime() : Infinity;
				data = data.filter(d => {
					const cand = d.date ? new Date(d.date).getTime() : NaN;
					if (isNaN(cand)) return true; // keep if no date field
					return cand >= from && cand <= to;
				});
			}

			// department filter best-effort
			if (this.department) {
				const key = 'department';
				data = data.filter(d => (d[key] || '').toString().toLowerCase().includes(this.department!.toLowerCase()));
			}

			this.lastResult = data;

			if (this.format === 'csv') {
				this.downloadCSVFromArray(data, `${this.selectedType}-report.csv`);
			} else {
				// generate a minimal HTML preview for PDF printing
				const rows = data.map(d => `<tr>${Object.values(d).map(v=>`<td>${v}</td>`).join('')}</tr>`).join('');
				const headers = data.length ? Object.keys(data[0]).map(h=>`<th>${h}</th>`).join('') : '';
				const html = `<html><head><meta charset="utf-8"><title>Rapport</title><style>table{border-collapse:collapse;width:100%}th,td{border:1px solid #ddd;padding:8px;text-align:left}</style></head><body><h1>Rapport: ${this.selectedType}</h1><p>Généré le ${new Date().toLocaleString()}</p><table><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table></body></html>`;
				this.printHTML(html);
			}
		} catch (e){
			console.error(e);
			this.message = 'Erreur lors de la génération du rapport.';
		} finally {
			this.loading = false;
		}
	}

	async exportCSV(){
		this.downloadCSVFromArray(this.lastResult.length ? this.lastResult : [{ id: '1', name: 'Exemple' }]);
	}

	async exportPDF(){
		const data = this.lastResult.length ? this.lastResult : [{ id: '1', name: 'Exemple' }];
		const rows = data.map(d => `<tr>${Object.values(d).map(v=>`<td>${v}</td>`).join('')}</tr>`).join('');
		const headers = data.length ? Object.keys(data[0]).map(h=>`<th>${h}</th>`).join('') : '';
		const html = `<html><head><meta charset="utf-8"><title>Rapport</title><style>table{border-collapse:collapse;width:100%}th,td{border:1px solid #ddd;padding:8px;text-align:left}</style></head><body><h1>Rapport: ${this.selectedType}</h1><p>Généré le ${new Date().toLocaleString()}</p><table><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table></body></html>`;
		this.printHTML(html);
	}
}
