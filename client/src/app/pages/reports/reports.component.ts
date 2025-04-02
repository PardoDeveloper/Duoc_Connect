import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { ReportesService } from '../../services/reportes.service'; // Asegúrate de tener este servicio creado

@Component({
  selector: 'app-reportes',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.css']
})
export class ReportesComponent {
  form = {
    tipo: '',
    descripcion: '',
    laboratorio: ''
  };

  tipos = [
    { value: 'equipo_danado', label: 'Equipo dañado' },
    { value: 'acoso', label: 'Acoso' },
    { value: 'bullying', label: 'Bullying' },
    { value: 'reclamo', label: 'Reclamo' },
    { value: 'coordinacion', label: 'Contacto con coordinación' }
  ];

  selectedFile: File | null = null;
  mensaje = '';

  constructor(private reportesService: ReportesService) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0] || null;
  }

  enviarReporte() {
    if (!this.form.tipo || !this.form.descripcion) {
      this.mensaje = 'Por favor completa los campos obligatorios.';
      return;
    }

    const formData = new FormData();
    formData.append('tipo', this.form.tipo);
    formData.append('descripcion', this.form.descripcion);
    if (this.form.laboratorio) {
      formData.append('laboratorio', this.form.laboratorio);
    }
    if (this.selectedFile) {
      formData.append('evidencia', this.selectedFile);
    }

    this.reportesService.enviarReporte(formData).subscribe({
      next: () => {
        this.mensaje = 'Reporte enviado correctamente.';
        this.form = { tipo: '', descripcion: '', laboratorio: '' };
        this.selectedFile = null;
      },
      error: () => {
        this.mensaje = 'Error al enviar el reporte.';
      }
    });
  }
}
