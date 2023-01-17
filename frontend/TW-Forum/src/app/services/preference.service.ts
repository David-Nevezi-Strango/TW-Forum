import { Injectable } from '@angular/core';
import { Observable,of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Tag } from 'src/models/tag';
import { Preference } from 'src/models/Preference';

@Injectable({
  providedIn: 'root'
})
export class PreferenceService {

  constructor(private http: HttpClient) { }
  url="http://localhost:5000/preferences"

  getPreferences():Observable<Preference[]>{
    return this.http.get<Preference[]>("http://localhost:5000/preferences")
  }
}
