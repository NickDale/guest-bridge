import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-accommodation-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.css']
})
export class ConfigComponent {
  @Input() accommodationId?: number;
}

