import { DatePipe } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { NgxSpinnerService } from 'ngx-spinner';
import { TierService } from 'src/app/core/service/tier.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  myDate = new Date();
  customerCount: number = 0;

  constructor(
    private spinner: NgxSpinnerService,
    private tierService: TierService) { }

  ngOnInit(): void {
    this.getCreatedList();
  }

  getCreatedList() {
    this.spinner.show();
    this.tierService.getCreatedList().subscribe({
      next: data => {
        this.customerCount = data.length;
        this.spinner.hide();
      },
      error: error => {
        this.spinner.hide();
        console.log(error);
      }
    });
  }
}
