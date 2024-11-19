import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface Record {
  marketing_year: string;
  area: number;
  yield: number;
  total_production: number;
  losses_and_feed: number;
  usable_production: number;
  fresh: {
    production: number;
    exports: number;
    imports: number;
    consumption: number;
    per_capita_production: number;
    ending_stocks: number;
    stock_change: number;
    self_sufficiency_rate: number;
  };
  processed: {
    production: number;
    exports: number;
    imports: number;
    consumption: number;
    per_capita_production: number;
    self_sufficiency_rate: number;
  };
  per_capita_production: number;
}

@Component({
  selector: 'app-records',
  templateUrl: './records.component.html',
  styleUrls: ['./records.component.css']
})
export class RecordsComponent implements OnInit {
  records: Record[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<Record[]>('/api/v1/apples/records').subscribe({
      next: (data) => (this.records = data),
      error: (error) => console.error('Failed to fetch records', error)
    });
  }
}
