import { Injectable } from '@angular/core';
import { Block } from './blocks';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class BlocksService {
  constructor(private http: HttpClient) { }

  getBlocks(): Observable<Block[]> {
    return this.http.get<Block[]>('http://localhost:8000/blocks');
  }

  getBlockById(id: number): Observable<Block> {
    return this.http.get<Block>(`http://localhost:8000/block/${id}`);
  }
}
