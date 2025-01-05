import { Injectable } from '@angular/core';
import { Block } from './blocks';

@Injectable({
  providedIn: 'root'
})
export class BlocksService {
  blocks: Block[] = [];

  constructor() { }

  getBlocks(): Block[] {
    let i = 0;
    while (i <= 50) {
      i++;
      this.blocks.push(new Block({
        id: 0,
        name: 'air',
        displayName: 'Air',
        hardness: 0.0,
        resistance: 0.0,
        stackSize: 64,
        diggable: false,
        material: 'default',
        transparent: true,
        emitLight: 0,
      }),);
    }

    return this.blocks;
  }
}
