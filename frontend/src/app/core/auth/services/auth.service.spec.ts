import { AuthService } from './auth.service';

describe('AuthService', () => {
  it('should be created', () => {
    const s = new AuthService();
    expect(s).toBeTruthy();
  });
});
