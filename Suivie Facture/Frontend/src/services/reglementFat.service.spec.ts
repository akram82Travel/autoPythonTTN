import { TestBed } from '@angular/core/testing';

import { reglementFatService } from './reglementFat.service';

describe('modePaiementService', () => {
  let service: reglementFatService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(reglementFatService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
