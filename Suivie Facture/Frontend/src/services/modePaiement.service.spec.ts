import { TestBed } from '@angular/core/testing';

import { modePaiementService } from './modePaiement.service';

describe('modePaiementService', () => {
  let service: modePaiementService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(modePaiementService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
