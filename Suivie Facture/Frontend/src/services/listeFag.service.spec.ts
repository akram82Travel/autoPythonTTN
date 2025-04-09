import { TestBed } from '@angular/core/testing';

import { listeFagService } from './listeFag.service';

describe('listeFagService', () => {
  let service: listeFagService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(listeFagService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
