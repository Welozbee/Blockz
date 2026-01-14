import { Injectable } from '@angular/core';
import { Block } from './blocks';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable()
export class BlocksService {
  constructor(private http: HttpClient, private authService: AuthService) { }

  getBlocks(): Observable<Block[]> {
    return this.http.get<Block[]>('/blocks');
  }

  getBlockById(id: number): Observable<Block> {
    return this.http.get<Block>(`/block/${id}`);
  }

  createBlock(block: Block): Observable<Block> {
    return this.http.post<Block>('/block', block, { headers: this.getAuthHeaders() });
  }

  updateBlock(id: number, block: Block): Observable<Block> {
    return this.http.put<Block>(`/block/${id}`, block, { headers: this.getAuthHeaders() });
  }

  uploadBlockImage(id: number, file: File): Observable<Block> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<Block>(`/block/${id}/image`, formData, { headers: this.getAuthHeaders() });
  }

  private getAuthHeaders(): HttpHeaders {
    const token = this.authService.getToken();
    return token ? new HttpHeaders({ Authorization: `Bearer ${token}` }) : new HttpHeaders();
  }
}
