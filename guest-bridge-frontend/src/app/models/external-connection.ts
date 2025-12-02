export interface ExternalLoginResponse {
    session_id: string
}
export interface SessionStatusResponse {
    session_id: string
    step: string;
}