import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AccomodationRegistrationFormComponent } from './accomodation-registration-form.component';

describe('AccomodationRegistrationFormComponent', () => {
  let component: AccomodationRegistrationFormComponent;
  let fixture: ComponentFixture<AccomodationRegistrationFormComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AccomodationRegistrationFormComponent]
    });
    fixture = TestBed.createComponent(AccomodationRegistrationFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
