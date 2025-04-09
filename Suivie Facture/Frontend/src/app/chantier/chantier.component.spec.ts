import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChantierComponent } from './chantier.component';

describe('ChantierComponent', () => {
  let component: ChantierComponent;
  let fixture: ComponentFixture<ChantierComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ChantierComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ChantierComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
