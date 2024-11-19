import { Routes } from '@angular/router';

import { UploadComponent } from './upload/upload.component';
import { RecordsComponent } from './records/records.component';

export const routes: Routes = [
  { path: '', redirectTo: '/upload', pathMatch: 'full' },
  { path: 'upload', component: UploadComponent },
  { path: 'records', component: RecordsComponent }
];
