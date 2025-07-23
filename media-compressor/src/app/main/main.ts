import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UploadComponent } from '../upload/upload';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, UploadComponent],
  templateUrl: './main.html',
  styleUrls: ['./main.scss']
})
export class MainComponent {}