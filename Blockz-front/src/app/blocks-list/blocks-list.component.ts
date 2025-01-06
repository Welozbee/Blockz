import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
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

  ngOnInit(): void {
    this.blocksService.getBlocks().subscribe({
      next: (res: Block[]) => {
        this.blocks = res;
      }
    });
  }
}
