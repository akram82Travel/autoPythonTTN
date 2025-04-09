import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListeReglementComponent } from './liste-reglement.component';

describe('ListeReglementComponent', () => {
  let component: ListeReglementComponent;
  let fixture: ComponentFixture<ListeReglementComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ListeReglementComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListeReglementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
