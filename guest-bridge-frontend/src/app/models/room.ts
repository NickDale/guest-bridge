export interface MapRecord {
  id: number;
  szallas_hu_ext_room_id: string;
  szallas_hu_ext_room_name: string;
  vendegem_ext_room_id: string | null; // Lehet null, ha nincs mappelés
  vendegem_ext_room_name: string | null; // Lehet null, ha nincs mappelés
  created_date: Date;
}

// A komponensben használt szoba interface-eket újradefiniáljuk
export interface Room {
  id: number; // Egyedi azonosító a belső kezeléshez
  externalId: string | null; // Külső (Szallas.hu/Vendégem) azonosító
  name: string | null;
}

// Mivel az ID-k stringek, a mapping is string alapú lesz
export interface RoomMapping {
    [szallasHuId: string]: string; // SzH ID -> VG ID
}

export interface MappedViewItem {
    szallasHuRoom: Room;
    vendegemRoom: Room | null; // Null, ha nincs mappelés
}