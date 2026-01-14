import { CommonModule } from '@angular/common';
import { Component, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BlocksListComponent } from "./blocks-list/blocks-list.component";
import { LoginComponent } from "./login/login.component";
import { AuthService } from './auth.service';
import { Block } from './blocks';
import { BlockEditorComponent } from './block-editor/block-editor.component';

@Component({
  selector: 'app-root',
  imports: [
    CommonModule,
    FormsModule,
    BlocksListComponent,
    BlockEditorComponent,
    LoginComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'blockz';
  @ViewChild(LoginComponent) loginComponent?: LoginComponent;
  @ViewChild(BlocksListComponent) blocksListComponent?: BlocksListComponent;
  @ViewChild(BlockEditorComponent) blockEditorComponent?: BlockEditorComponent;
  showLogoutConfirm = false;
  selectedBlock: Block | null = null;
  filterText = '';
  filterDiggable: 'all' | 'yes' | 'no' = 'all';
  filterTransparent: 'all' | 'yes' | 'no' = 'all';

  constructor(private authService: AuthService) {}

  get isLoggedIn(): boolean {
    return this.authService.isLoggedIn();
  }

  get isAdmin(): boolean {
    return this.authService.isAdmin();
  }

  get username(): string | null {
    return this.authService.getUsername();
  }

  get displayName(): string {
    return this.username ?? 'Compte';
  }

  openLogin(): void {
    if (this.loginComponent) {
      this.loginComponent.open();
      this.loginComponent.setDefaultUsername(this.username);
    }
  }

  onBlockSelected(block: Block): void {
    this.selectedBlock = block;
  }

  openCreateBlock(): void {
    if (this.blockEditorComponent) {
      this.blockEditorComponent.openCreate();
    }
  }

  openEditBlock(): void {
    if (this.blockEditorComponent && this.selectedBlock) {
      this.blockEditorComponent.openEdit(this.selectedBlock);
    }
  }

  onBlockSaved(): void {
    this.selectedBlock = null;
    this.blocksListComponent?.reload();
  }

  onEditorClosed(): void {
    this.blocksListComponent?.reload();
  }

  openLogoutConfirm(): void {
    this.showLogoutConfirm = true;
  }

  closeLogoutConfirm(): void {
    this.showLogoutConfirm = false;
  }

  confirmLogout(): void {
    this.authService.logout();
    this.showLogoutConfirm = false;
  }
}
