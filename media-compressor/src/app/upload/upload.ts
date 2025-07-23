import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './upload.html',
  styleUrls: ['./upload.scss']
})
export class UploadComponent {
  selectedFiles: File[] = [];

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    this.selectedFiles = Array.from(event.target.files);
  }

  uploadFiles() {
    const formData = new FormData();
    this.selectedFiles.forEach(file => formData.append('files', file));

    this.http.post('http://localhost:5000/upload', formData, {
      responseType: 'blob',
      observe: 'response'
    })
    .subscribe(response => {
      const blob = response.body;

      // Extrair nome do header
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = 'ficheiro_comprimido';

      if (contentDisposition) {
        // Expressão regular que cobre aspas, pontos e espaços
        const match = contentDisposition.match(/filename\*?=(?:UTF-8'')?["]?([^;"\n]+)["]?/);
        if (match && match[1]) {
            filename = match[1].trim();
          }
      }

      if (blob) {
        const downloadUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(downloadUrl);
      }
    });
  }
}