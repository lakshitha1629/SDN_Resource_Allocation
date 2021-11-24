import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class TierService {

  constructor(private readonly http: HttpClient) { }

  getCreatedList(): Observable<any> {
    return this.http.get<any>(`${environment.apiUrl}api/getAllList`);
  }

  getSuggestion(predictData: any) {
    return this.http.post<any>(`${environment.apiUrl}api/getSuggestion`, predictData);
  }

  createTier(tierType: number) {
    return this.http.post<any>(`${environment.apiUrl}api/createTier`, tierType);
  }


}
