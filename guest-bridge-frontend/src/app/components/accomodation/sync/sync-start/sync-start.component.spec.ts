import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SyncStartComponent } from './sync-start.component';

describe('SyncStartComponent', () => {
  let component: SyncStartComponent;
  let fixture: ComponentFixture<SyncStartComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SyncStartComponent]
    });
    fixture = TestBed.createComponent(SyncStartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
