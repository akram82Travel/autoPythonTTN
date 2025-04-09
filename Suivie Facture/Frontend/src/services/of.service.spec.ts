import { TestBed } from '@angular/core/testing';

import { OfService } from './of.service';

describe('OfService', () => {
  let service: OfService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(OfService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
