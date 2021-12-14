import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnapprovedUsersComponent } from './unapproved-users.component';

describe('UnapprovedUsersComponent', () => {
  let component: UnapprovedUsersComponent;
  let fixture: ComponentFixture<UnapprovedUsersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnapprovedUsersComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UnapprovedUsersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
