import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { BlocksListComponent } from "./blocks-list/blocks-list.component";

@Component({
  selector: 'app-root',
  imports: [
    BlocksListComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'blockz';
}
