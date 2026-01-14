import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { Block } from '../blocks';
import { BlocksService } from '../blocks.service';

@Component({
  selector: 'app-blocks-list',
  imports: [
    MatCardModule,
    CommonModule
  ],
  templateUrl: './blocks-list.component.html',
  styleUrl: './blocks-list.component.scss'
})
export class BlocksListComponent implements OnInit {
  constructor(
    private blocksService: BlocksService,
  ) { }

  blocks: Block[] = [];
  @Input() selectedId: number | null = null;
  @Input() filterText = '';
  @Input() filterDiggable: 'all' | 'yes' | 'no' = 'all';
  @Input() filterTransparent: 'all' | 'yes' | 'no' = 'all';
  @Output() selected = new EventEmitter<Block>();

  ngOnInit(): void {
    this.reload();
  }

  reload(): void {
    this.blocksService.getBlocks().subscribe({
      next: (res: Block[]) => {
        this.blocks = res;
      }
    });
  }

  selectBlock(block: Block): void {
    this.selectedId = block.id;
    this.selected.emit(block);
  }

  get filteredBlocks(): Block[] {
    const text = this.filterText.trim().toLowerCase();
    return this.blocks.filter((block) => {
      if (text) {
        const match = `${block.name} ${block.displayName} ${block.material}`.toLowerCase();
        if (!match.includes(text)) {
          return false;
        }
      }
      if (this.filterDiggable !== 'all') {
        const desired = this.filterDiggable === 'yes';
        if (block.diggable !== desired) {
          return false;
        }
      }
      if (this.filterTransparent !== 'all') {
        const desired = this.filterTransparent === 'yes';
        if (block.transparent !== desired) {
          return false;
        }
      }
      return true;
    });
  }
}
