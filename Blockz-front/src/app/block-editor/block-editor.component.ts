import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Block } from '../blocks';
import { BlocksService } from '../blocks.service';

type EditorMode = 'create' | 'edit';

@Component({
  selector: 'app-block-editor',
  imports: [CommonModule, FormsModule],
  templateUrl: './block-editor.component.html',
  styleUrl: './block-editor.component.scss'
})
export class BlockEditorComponent {
  @Output() saved = new EventEmitter<void>();
  @Output() closed = new EventEmitter<void>();

  isOpen = false;
  mode: EditorMode = 'create';
  errorMessage = '';
  isSaving = false;
  selectedFile: File | null = null;

  form: Block = new Block({
    id: 0,
    name: '',
    displayName: '',
    hardness: 0,
    resistance: 0,
    stackSize: 64,
    diggable: true,
    material: '',
    transparent: false,
    emitLight: 0
  });

  constructor(private blocksService: BlocksService) {}

  openCreate(): void {
    this.mode = 'create';
    this.form = new Block({
      id: 0,
      name: '',
      displayName: '',
      hardness: 0,
      resistance: 0,
      stackSize: 64,
      diggable: true,
      material: '',
      transparent: false,
      emitLight: 0
    });
    this.errorMessage = '';
    this.selectedFile = null;
    this.isOpen = true;
  }

  openEdit(block: Block): void {
    this.mode = 'edit';
    this.form = new Block(block);
    this.errorMessage = '';
    this.selectedFile = null;
    this.isOpen = true;
  }

  close(): void {
    this.isOpen = false;
    this.selectedFile = null;
    this.closed.emit();
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0] ?? null;
    if (!file) {
      this.selectedFile = null;
      return;
    }
    const allowed = ['image/png', 'image/jpeg', 'image/webp'];
    if (!allowed.includes(file.type)) {
      this.errorMessage = 'Format invalide (png, jpg, webp).';
      this.selectedFile = null;
      input.value = '';
      return;
    }
    if (file.size > 2_000_000) {
      this.errorMessage = 'Image trop volumineuse (2 Mo max).';
      this.selectedFile = null;
      input.value = '';
      return;
    }
    this.errorMessage = '';
    this.selectedFile = file;
  }

  submit(): void {
    const validation = this.validate();
    if (validation) {
      this.errorMessage = validation;
      return;
    }

    this.isSaving = true;
    const payload = new Block({
      id: Number(this.form.id),
      name: this.form.name.trim(),
      displayName: this.form.displayName.trim(),
      hardness: Number(this.form.hardness),
      resistance: Number(this.form.resistance),
      stackSize: Number(this.form.stackSize),
      diggable: Boolean(this.form.diggable),
      material: this.form.material.trim(),
      transparent: Boolean(this.form.transparent),
      emitLight: Number(this.form.emitLight)
    });

    const request = this.mode === 'create'
      ? this.blocksService.createBlock(payload)
      : this.blocksService.updateBlock(payload.id, payload);

    request.subscribe({
      next: (saved) => {
        if (this.selectedFile) {
          this.blocksService.uploadBlockImage(saved.id, this.selectedFile).subscribe({
            next: () => {
              this.finishSave();
            },
            error: () => {
              this.isSaving = false;
              this.errorMessage = 'Erreur lors de l\'upload de l\'image.';
            }
          });
          return;
        }
        this.finishSave();
      },
      error: () => {
        this.isSaving = false;
        this.errorMessage = 'Erreur lors de la sauvegarde.';
      }
    });
  }

  private finishSave(): void {
    this.isSaving = false;
    this.isOpen = false;
    this.selectedFile = null;
    this.saved.emit();
  }

  private validate(): string | null {
    if (!this.form.name?.trim() || !this.form.displayName?.trim() || !this.form.material?.trim()) {
      return 'Nom, affichage et materiau requis.';
    }

    const hardness = Number(this.form.hardness);
    const resistance = Number(this.form.resistance);
    const stackSize = Number(this.form.stackSize);
    const emitLight = Number(this.form.emitLight);

    if (Number.isNaN(hardness) || hardness < -1) {
      return 'Durabilite invalide (min -1).';
    }
    if (this.form.diggable && hardness === -1) {
      return 'Un bloc creusable ne peut pas etre incassable.';
    }
    if (Number.isNaN(resistance) || resistance < 0) {
      return 'Resistance invalide (min 0).';
    }
    if (Number.isNaN(stackSize) || stackSize < 1 || stackSize > 64) {
      return 'Stack invalide (1-64).';
    }
    if (Number.isNaN(emitLight) || emitLight < 0 || emitLight > 15) {
      return 'Lumiere invalide (0-15).';
    }
    return null;
  }
}
