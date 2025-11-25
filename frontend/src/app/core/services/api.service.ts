import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BASE_API } from '../../app.api';

@Injectable({
	providedIn: 'root'
})
export class ApiService {
	private base = BASE_API;

	constructor(private http: HttpClient) {}

		get<T>(path: string, params?: Record<string, any>, options?: { responseType?: 'json' | 'blob' | 'text' | 'arraybuffer' }): Observable<T> {
		let httpParams = new HttpParams();
		if (params) {
			Object.keys(params).forEach(k => {
				const v = params![k];
				if (v !== undefined && v !== null) httpParams = httpParams.set(k, String(v));
			});
		}
		const url = path.startsWith('http') ? path : `${this.base}${path.startsWith('/') ? path : '/' + path}`;
			const responseType = options?.responseType ?? 'json';
			if (responseType === 'json') {
				return this.http.get<T>(url, { params: httpParams }) as Observable<T>;
			}
			// For non-json response types we need to cast appropriately
			return this.http.get(url, { params: httpParams, responseType: responseType as any }) as Observable<T>;
	}

	post<T>(path: string, body: any): Observable<T> {
		const url = path.startsWith('http') ? path : `${this.base}${path.startsWith('/') ? path : '/' + path}`;
		return this.http.post<T>(url, body);
	}

	put<T>(path: string, body: any): Observable<T> {
		const url = path.startsWith('http') ? path : `${this.base}${path.startsWith('/') ? path : '/' + path}`;
		return this.http.put<T>(url, body);
	}

	patch<T>(path: string, body: any): Observable<T> {
		const url = path.startsWith('http') ? path : `${this.base}${path.startsWith('/') ? path : '/' + path}`;
		return this.http.patch<T>(url, body);
	}

	delete<T>(path: string): Observable<T> {
		const url = path.startsWith('http') ? path : `${this.base}${path.startsWith('/') ? path : '/' + path}`;
		return this.http.delete<T>(url);
	}
}
