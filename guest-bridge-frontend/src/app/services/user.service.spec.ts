import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { UserService } from './user.service';
import { environment } from 'src/enviroments/environment';
import { User, UpdateUserRequest } from '../models/user';

describe('UserService', () => {
  let service: UserService;
  let httpMock: HttpTestingController;
  const apiUrl = environment.apiUrl;

  const mockUser: User = {
    id: 1,
    full_name: 'Test User',
    username: 'testuser',
    email: 'test@example.com',
    status: 'active',
    type: 'user',
    subscription_type: 'premium',
    activation_date: new Date('2024-01-01'),
    blocked_date: new Date('2024-12-31'),
    created_date: new Date('2023-01-01'),
    number_of_accommodations: 5,
    billing_info: {
      id: 1,
      name: 'Test Billing',
      email: 'billing@example.com',
      tax: '12345678-1-23',
      postcode: '1011',
      country: 'Hungary',
      city: 'Budapest',
      street: 'Test utca',
      street_number: '1',
      floor: '2',
      door: '3'
    }
  };

  const mockUsers: User[] = [
    mockUser,
    {
      id: 2,
      full_name: 'Another User',
      username: 'anotheruser',
      email: 'another@example.com',
      status: 'inactive',
      type: 'admin',
      subscription_type: 'basic',
      activation_date: new Date('2024-02-01'),
      blocked_date: new Date('2024-12-31'),
      created_date: new Date('2023-02-01'),
      number_of_accommodations: 2,
      billing_info: {
        id: 2,
        name: 'Another Billing',
        email: 'another-billing@example.com',
        tax: '87654321-2-45',
        postcode: '4025',
        country: 'Hungary',
        city: 'Debrecen',
        street: 'Másik utca',
        street_number: '2',
        floor: '1',
        door: '5'
      }
    }
  ];

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService]
    });
    service = TestBed.inject(UserService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('users array', () => {
    it('should initialize with empty array', () => {
      expect(service.users).toEqual([]);
      expect(Array.isArray(service.users)).toBe(true);
    });
  });

  describe('mockedData', () => {
    it('should return users array', () => {
      service.users = mockUsers;
      const result = service.mockedData();
      expect(result).toEqual(mockUsers);
      expect(result.length).toBe(2);
    });

    it('should return empty array when no users', () => {
      const result = service.mockedData();
      expect(result).toEqual([]);
    });
  });

  describe('listUsers', () => {
    it('should call correct endpoint with expect parameter', () => {
      service.listUsers().subscribe();

      const req = httpMock.expectOne(`${apiUrl}/users?expect=admin`);
      expect(req.request.method).toBe('GET');
      expect(req.request.urlWithParams).toContain('expect=admin');
      req.flush(mockUsers);
    });

    it('should return list of users', (done) => {
      service.listUsers().subscribe(users => {
        expect(users).toEqual(mockUsers);
        expect(users.length).toBe(2);
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/users?expect=admin`);
      req.flush(mockUsers);
    });

    it('should handle empty user list', (done) => {
      service.listUsers().subscribe(users => {
        expect(users).toEqual([]);
        expect(users.length).toBe(0);
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/users?expect=admin`);
      req.flush([]);
    });
  });

  describe('getUserById', () => {
    it('should call correct endpoint with user id', () => {
      const userId = 1;
      service.getUserById(userId).subscribe();

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}`);
      expect(req.request.method).toBe('GET');
      req.flush(mockUser);
    });

    it('should return single user', (done) => {
      const userId = 1;
      service.getUserById(userId).subscribe(user => {
        expect(user).toEqual(mockUser);
        expect(user.id).toBe(1);
        expect(user.full_name).toBe('Test User');
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}`);
      req.flush(mockUser);
    });

    it('should handle different user ids', (done) => {
      const userId = 999;
      const differentUser = { ...mockUser, id: 999, full_name: 'Different User' };

      service.getUserById(userId).subscribe(user => {
        expect(user.id).toBe(999);
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}`);
      req.flush(differentUser);
    });
  });

  describe('selectedUser$ observable', () => {
    it('should initialize with null', (done) => {
      service.selectedUser$.subscribe(user => {
        expect(user).toBeNull();
        done();
      });
    });

    it('should emit new value when setSelectedUser is called', (done) => {
      let emissionCount = 0;
      service.selectedUser$.subscribe(user => {
        emissionCount++;
        if (emissionCount === 2) {
          expect(user).toEqual(mockUser);
          done();
        }
      });

      service.setSelectedUser(mockUser);
    });

    it('should emit null when setSelectedUser is called with null', (done) => {
      let emissionCount = 0;
      service.selectedUser$.subscribe(user => {
        emissionCount++;
        if (emissionCount === 2) {
          expect(user).toBeNull();
          done();
        }
      });

      service.setSelectedUser(null as any);
    });

    it('should emit multiple values in sequence', (done) => {
      const values: (User | null)[] = [];
      service.selectedUser$.subscribe(user => {
        values.push(user);
        if (values.length === 3) {
          expect(values[0]).toBeNull();
          expect(values[1]).toEqual(mockUser);
          expect(values[2]).toEqual(mockUsers[1]);
          done();
        }
      });

      service.setSelectedUser(mockUser);
      service.setSelectedUser(mockUsers[1]);
    });
  });

  describe('updateUser', () => {
    it('should call correct endpoint with PATCH method', () => {
      const userId = 1;
      const updateRequest: UpdateUserRequest = {
        full_name: 'Updated Name',
        email: 'updated@example.com',
        billing_info: {
          id: 1,
          name: 'Updated Billing',
          email: 'updated-billing@example.com',
          tax: '11111111-1-11',
          postcode: '1011',
          country: 'Hungary',
          city: 'Budapest',
          street: 'Updated utca',
          street_number: '1',
          floor: '3',
          door: '4'
        }
      };

      service.updateUser(userId, updateRequest).subscribe();

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}`);
      expect(req.request.method).toBe('PATCH');
      expect(req.request.body).toEqual(updateRequest);
      req.flush(null);
    });

    it('should return true on successful update', (done) => {
      const userId = 1;
      const updateRequest: UpdateUserRequest = {
        full_name: 'Updated Name',
        email: 'updated@example.com',
        billing_info: {
          id: 1,
          name: 'Updated Billing',
          email: 'updated-billing@example.com',
          tax: '11111111-1-11',
          postcode: '1011',
          country: 'Hungary',
          city: 'Budapest',
          street: 'Updated utca',
          street_number: '1',
          floor: '3',
          door: '4'
        }
      };

      service.updateUser(userId, updateRequest).subscribe(result => {
        expect(result).toBe(true);
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}`);
      req.flush(null);
    });

    it('should handle error and throw', (done) => {
      const userId = 1;
      const updateRequest: UpdateUserRequest = {
        full_name: 'Updated Name',
        email: 'updated@example.com',
        billing_info: {
          id: 1,
          name: 'Updated Billing',
          email: 'updated-billing@example.com',
          tax: '11111111-1-11',
          postcode: '1011',
          country: 'Hungary',
          city: 'Budapest',
          street: 'Updated utca',
          street_number: '1',
          floor: '3',
          door: '4'
        }
      };
      const errorMessage = 'Update failed';

      service.updateUser(userId, updateRequest).subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(500);
          done();
        }
      });

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}`);
      req.flush(errorMessage, { status: 500, statusText: 'Internal Server Error' });
    });
  });

  describe('changePassword', () => {
    it('should call correct endpoint with password data', () => {
      const userId = 1;
      const oldPassword = 'oldpass123';
      const newPassword = 'newpass456';

      service.changePassword(userId, oldPassword, newPassword).subscribe();

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}/change-password`);
      expect(req.request.method).toBe('PATCH');
      expect(req.request.body).toEqual({
        old_password: oldPassword,
        new_password: newPassword
      });
      req.flush(null);
    });

    it('should return true on successful password change', (done) => {
      const userId = 1;
      service.changePassword(userId, 'old', 'new').subscribe(result => {
        expect(result).toBe(true);
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}/change-password`);
      req.flush(null);
    });

    it('should handle error on password change', (done) => {
      const userId = 1;
      service.changePassword(userId, 'wrong', 'new').subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(401);
          done();
        }
      });

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}/change-password`);
      req.flush('Invalid password', { status: 401, statusText: 'Unauthorized' });
    });
  });

  describe('registerUser', () => {
    it('should call correct endpoint with user data', () => {
      const name = 'New User';
      const email = 'newuser@example.com';

      service.registerUser(name, email).subscribe();

      const req = httpMock.expectOne(`${apiUrl}/users`);
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual({ name, email });
      req.flush(null);
    });

    it('should return true on successful registration', (done) => {
      service.registerUser('Test', 'test@test.com').subscribe(result => {
        expect(result).toBe(true);
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/users`);
      req.flush(null);
    });

    it('should handle registration error', (done) => {
      service.registerUser('Test', 'invalid-email').subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(400);
          done();
        }
      });

      const req = httpMock.expectOne(`${apiUrl}/users`);
      req.flush('Invalid email', { status: 400, statusText: 'Bad Request' });
    });
  });

  describe('deactivate', () => {
    it('should call correct endpoint with DELETE method', () => {
      const userId = 1;
      service.deactivate(userId).subscribe();

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}/inactivate`);
      expect(req.request.method).toBe('DELETE');
      req.flush(null);
    });

    it('should return true on successful deactivation', (done) => {
      const userId = 1;
      service.deactivate(userId).subscribe(result => {
        expect(result).toBe(true);
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}/inactivate`);
      req.flush(null);
    });

    it('should handle deactivation error', (done) => {
      const userId = 1;
      service.deactivate(userId).subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(404);
          done();
        }
      });

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}/inactivate`);
      req.flush('User not found', { status: 404, statusText: 'Not Found' });
    });
  });

  describe('activate', () => {
    it('should call correct endpoint with PATCH method', () => {
      const userId = 1;
      service.activate(userId).subscribe();

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}/activate`);
      expect(req.request.method).toBe('PATCH');
      expect(req.request.body).toEqual({});
      req.flush(null);
    });

    it('should return true on successful activation', (done) => {
      const userId = 1;
      service.activate(userId).subscribe(result => {
        expect(result).toBe(true);
        done();
      });

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}/activate`);
      req.flush(null);
    });

    it('should handle activation error', (done) => {
      const userId = 1;
      service.activate(userId).subscribe({
        next: () => fail('should have failed'),
        error: (error) => {
          expect(error.status).toBe(403);
          done();
        }
      });

      const req = httpMock.expectOne(`${apiUrl}/users/${userId}/activate`);
      req.flush('Forbidden', { status: 403, statusText: 'Forbidden' });
    });
  });

  describe('Integration scenarios', () => {
    it('should handle full user lifecycle', (done) => {
      let step = 0;

      // Step 1: Register
      service.registerUser('New User', 'new@test.com').subscribe(result => {
        expect(result).toBe(true);
        step++;
        if (step === 4) done();
      });
      const registerReq = httpMock.expectOne(`${apiUrl}/users`);
      registerReq.flush(null);

      // Step 2: Get user
      service.getUserById(1).subscribe(user => {
        expect(user.id).toBe(1);
        step++;
        if (step === 4) done();
      });
      const getUserReq = httpMock.expectOne(`${apiUrl}/users/1`);
      getUserReq.flush(mockUser);

      // Step 3: Update user
      const updateReq: UpdateUserRequest = {
        full_name: 'Updated',
        email: 'updated@test.com',
        billing_info: {
          id: 1,
          name: 'Updated Billing',
          email: 'billing@test.com',
          tax: '99999999-9-99',
          postcode: '1011',
          country: 'Hungary',
          city: 'Budapest',
          street: 'Test',
          street_number: '1',
          floor: '2',
          door: '3'
        }
      };
      service.updateUser(1, updateReq).subscribe(result => {
        expect(result).toBe(true);
        step++;
        if (step === 4) done();
      });
      const updateUserReq = httpMock.expectOne(`${apiUrl}/users/1`);
      updateUserReq.flush(null);

      // Step 4: Deactivate
      service.deactivate(1).subscribe(result => {
        expect(result).toBe(true);
        step++;
        if (step === 4) done();
      });
      const deactivateReq = httpMock.expectOne(`${apiUrl}/users/1/inactivate`);
      deactivateReq.flush(null);
    });
  });
});