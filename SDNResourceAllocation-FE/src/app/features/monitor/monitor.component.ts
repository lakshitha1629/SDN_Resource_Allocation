import { Component, OnInit } from '@angular/core';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastrService } from 'ngx-toastr';
import { TierService } from 'src/app/core/service/tier.service';

@Component({
  selector: 'app-monitor',
  templateUrl: './monitor.component.html',
  styleUrls: ['./monitor.component.scss']
})
export class MonitorComponent implements OnInit {
  monitorDetails: any;
  constructor(
    private spinner: NgxSpinnerService,
    private tierService: TierService) { }

  ngOnInit(): void {
    this.getCreatedList();
  }

  getCreatedList() {
    this.spinner.show();
    this.tierService.getMonitorDetails().subscribe({
      next: data => {
        this.monitorDetails = data;
        this.spinner.hide();
      },
      error: error => {
        this.spinner.hide();
        console.log(error);
      }
    });
  }

}
