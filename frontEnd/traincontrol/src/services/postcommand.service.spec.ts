import {TestBed} from '@angular/core/testing';

import {PostcommandService} from './postcommand.service';

describe('PostcommandService', () => {
  let service: PostcommandService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PostcommandService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
