import { Component, OnInit } from '@angular/core';
import { NgModel } from '@angular/forms';

interface AppleRecord {
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
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-records',
  templateUrl: './records.component.html',
  styleUrls: ['./records.component.css']
})
export class RecordsComponent implements OnInit {
  records: AppleRecord[] = [];

  constructor(private http: HttpClient) {}

  saveRecords() {
    this.http.put('/api/v1/apples/records', this.records).subscribe({
      next: () => {
        console.log('Records saved successfully');
        alert('Records saved successfully');
      },
      error: (error) => {
        console.error('Failed to save records', error);
        alert('Failed to save records');
      }
    });
  }

  ngOnInit() {
    this.http.get<AppleRecord[]>('/api/v1/apples/records').subscribe({
      next: (data) => (this.records = data),
      error: (error) => console.error('Failed to fetch records', error)
    });
  }

  addRecord() {
    const newRecord: AppleRecord = {
      marketing_year: 'New Year',
      area: 0,
      yield: 0,
      total_production: 0,
      losses_and_feed: 0,
      usable_production: 0,
      fresh: {
        production: 0,
        exports: 0,
        imports: 0,
        consumption: 0,
        per_capita_production: 0,
        ending_stocks: 0,
        stock_change: 0,
        self_sufficiency_rate: 0
      },
      processed: {
        production: 0,
        exports: 0,
        imports: 0,
        consumption: 0,
        per_capita_production: 0,
        self_sufficiency_rate: 0
      },
      per_capita_production: 0
    };
    this.records.push(newRecord);
  }

  removeRecord(index: number) {
    this.records.splice(index, 1);
  }
}
