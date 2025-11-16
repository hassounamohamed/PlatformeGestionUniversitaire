import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-group-form-dialog',
  standalone: true,
  imports: [CommonModule, MatFormFieldModule, MatInputModule, MatButtonModule, ReactiveFormsModule],
  templateUrl: './group-form-dialog.component.html',
  styleUrls: ['./group-form-dialog.component.css']
})
export class GroupFormDialogComponent {
  form: any;

  constructor(private fb: FormBuilder, private dialogRef: MatDialogRef<GroupFormDialogComponent>) {
    this.form = this.fb.group({
      name: ['', [Validators.required, Validators.maxLength(100)]],
      code: ['', [Validators.required, Validators.maxLength(30)]],
      semester: [1, [Validators.required, Validators.min(1)]],
      maxCapacity: [30, [Validators.required, Validators.min(1)]],
    });
  }

  submit() {
    if (this.form.valid) {
      const value = this.form.value;
      // return the created group partial to the caller
      this.dialogRef.close({
        name: value.name,
        code: value.code,
        semester: value.semester,
        maxCapacity: value.maxCapacity,
        studentCount: 0,
        subjects: []
      });
    }
  }

  cancel() {
    this.dialogRef.close(null);
  }
}
