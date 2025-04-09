import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListeFagComponent } from './liste-fag.component';

describe('ListeFagComponent', () => {
  let component: ListeFagComponent;
  let fixture: ComponentFixture<ListeFagComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ListeFagComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListeFagComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
