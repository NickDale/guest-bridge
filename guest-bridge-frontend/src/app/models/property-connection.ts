export interface Property {
    id:number;
    type: ConnectionType;
    status: ConnectionStatus;
    lastCheck: Date;
}

export enum ConnectionStatus {
    SUCCESS = 'OK', 
    FAILED = ':('
}
export enum ConnectionType {
    SZALLAS_HU = 'Szallas.hu',
    VENDEGEM = 'Vendégem'
  }
  