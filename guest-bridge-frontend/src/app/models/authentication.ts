export interface LoggedUser {
  id: number;
  role: 'admin' | 'user';
  full_name: string
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: LoggedUser;
}
