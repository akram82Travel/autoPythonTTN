import { TestBed } from '@angular/core/testing';

import { FactureTTNService } from './FactureTTN.service';

describe('FactureTTNService', () => {
  let service: FactureTTNService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FactureTTNService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
