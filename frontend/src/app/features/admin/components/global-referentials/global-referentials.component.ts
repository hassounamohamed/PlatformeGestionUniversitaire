import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService } from '../../services/admin.service';

interface ReferentialItem {
	id?: string;
	name?: string;
	title?: string;
	email?: string;
	label?: string;
	[key: string]: any;
}

interface Section {
	key: string;
	title: string;
	items: ReferentialItem[];
}

@Component({
	selector: 'admin-global-referentials',
	standalone: true,
	imports: [CommonModule, FormsModule],
		templateUrl: './global-referentials.component.html',
		styleUrls: ['../../admin.styles.css', './global-referentials.component.css']
})
export class GlobalReferentialsComponent implements OnInit {
	sections: Section[] = [
		{ key: 'departments', title: 'Départements', items: [] },
		{ key: 'specialties', title: 'Spécialités', items: [] },
		{ key: 'teachers', title: 'Enseignants', items: [] },
		{ key: 'students', title: 'Étudiants', items: [] },
		{ key: 'rooms', title: 'Salles', items: [] },
		{ key: 'subjects', title: 'Matères', items: [] }
	];

	activeSection: Section = this.sections[0];

	// Inline add form state
	showAddForm = false;
	formModel: any = {};

	constructor(private admin: AdminService) {}

	ngOnInit(): void {
		this.loadAll();
	}

	setSection(section: Section) {
		this.activeSection = section;
	}

	async loadAll() {
		for (const s of this.sections) {
			try {
				// fetch from API via AdminService - falls back to empty list
				s.items = (await this.admin.list(s.key)) || [];
			} catch (e) {
				s.items = [];
			}
		}
	}

	async remove(item: ReferentialItem) {
		if (!confirm('Confirmer la suppression ?')) return;
		await this.admin.remove(this.activeSection.key, item.id);
		this.loadAll();
	}

	// lightweight add (prompt-based) to keep changes minimal

	// Show form instead of prompt
	async add() {
		this.showAddForm = true;
		this.formModel = {};
	}

	async submitAdd() {
		// map formModel to API payload per section
		let payload: any = {};
		switch (this.activeSection.key) {
			case 'departments':
				payload = { nom: this.formModel.nom || this.formModel.name };
				break;
			case 'specialties':
				payload = { nom: this.formModel.nom || this.formModel.name, departement_id: this.formModel.departement_id };
				break;
			case 'teachers':
				payload = { nom: this.formModel.nom, prenom: this.formModel.prenom, email: this.formModel.email, departement_id: this.formModel.departement_id };
				break;
			case 'students':
				payload = { nom: this.formModel.nom, prenom: this.formModel.prenom, email: this.formModel.email, groupe_id: this.formModel.groupe_id, specialite_id: this.formModel.specialite_id };
				break;
			case 'rooms':
				payload = { code: this.formModel.code || this.formModel.name, type: this.formModel.type, capacite: this.formModel.capacite };
				break;
			case 'subjects':
				payload = { nom: this.formModel.nom || this.formModel.name, niveau_id: this.formModel.niveau_id, enseignant_id: this.formModel.enseignant_id };
				break;
			default:
				payload = this.formModel;
		}

		try {
			const res = await this.admin.create(this.activeSection.key, payload);
			if (!res) {
				alert('Erreur lors de la création. Vérifiez la console et le backend.');
				return;
			}

			// After creating a teacher/student, also create an auth account so they can log in
			if (this.activeSection.key === 'teachers' || this.activeSection.key === 'students') {
				// helper to generate a random temporary password
				const randomPassword = (len = 10) => {
					const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()';
					let out = '';
					for (let i = 0; i < len; i++) out += chars.charAt(Math.floor(Math.random() * chars.length));
					return out;
				};

				const pwd = randomPassword(10);
				const namePart = (res.nom || res.name || payload.nom || payload.name || 'user').toString();
				const username = (namePart.replace(/\s+/g, '').toLowerCase()).slice(0, 30);
				const email = (res.email || payload.email || `${username}@example.com`).toString();
				const full_name = ((res.prenom || payload.prenom) ? `${res.prenom || payload.prenom} ` : '') + (res.nom || payload.nom || '');
				const role = this.activeSection.key === 'teachers' ? 'enseignant' : 'etudiant';

				const authPayload = {
					email,
					username,
					full_name: full_name.trim(),
					password: pwd,
					role
				};

				try {
					const createdAuth = await this.admin.registerAuth(authPayload);
					if (!createdAuth) {
						console.warn('Auth registration failed for', authPayload);
						alert('La fiche a été créée mais la création du compte de connexion a échoué. Voir console.');
					} else {
						// show the temporary password to admin and copy to clipboard if available
						const info = `Compte créé pour ${authPayload.email}\nMot de passe temporaire: ${pwd}`;
						try {
							navigator.clipboard && navigator.clipboard.writeText(pwd);
							alert(info + '\n(Mot de passe copié dans le presse-papier)');
						} catch (ex) {
							alert(info);
						}
					}
				} catch (e) {
					console.error('Error registering auth account', e);
					alert('La fiche a été créée mais création du compte d\'auth a échoué. Voir console.');
				}
			}

			// If the API returned the created item, optimistically update the local list
			this.showAddForm = false;
			try {
				// insert returned entity at top of its section for immediate visibility
				const target = this.sections.find(s => s.key === this.activeSection.key);
				if (target && res) {
					// normalize: some APIs return 'nom' while template reads ['nom'] or name
					target.items = [res, ...target.items];
				}
				// refresh from server to ensure consistency
				await this.loadAll();
			} catch (e) {
				console.warn('Refresh after create failed', e);
			}
		} catch (err) {
			console.error('Create error', err);
			alert('Erreur lors de la création. Voir console pour détails.');
		}
	}

	cancelAdd() {
		this.showAddForm = false;
		this.formModel = {};
	}
}
