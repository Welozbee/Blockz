import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BlocksListComponent } from './blocks-list.component';

describe('BlocksListComponent', () => {
  let component: BlocksListComponent;
  let fixture: ComponentFixture<BlocksListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BlocksListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BlocksListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
