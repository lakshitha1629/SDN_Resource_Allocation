import { Component, OnInit } from '@angular/core';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastrService } from 'ngx-toastr';
import { TierService } from 'src/app/core/service/tier.service';

@Component({
  selector: 'app-tiers-list',
  templateUrl: './tiers-list.component.html',
  styleUrls: ['./tiers-list.component.scss']
})
export class TiersListComponent implements OnInit {
  dataList = [];
  selectedItems = [];
  isBestResult: boolean = false;
  tierData: any;
  result: any;

  constructor(
    private toastr: ToastrService,
    private spinner: NgxSpinnerService,
    private tierService: TierService) { }

  ngOnInit(): void {
    this.getCreatedList();
  }

  getCreatedList() {
    this.spinner.show();
    this.tierService.getCreatedList().subscribe({
      next: data => {
        this.dataList = data;
        this.spinner.hide();
      },
      error: error => {
        this.spinner.hide();
        console.log(error);
        this.toastr.error(error.error.detail);
      }
    });
  }

  sendTraffic() {
    this.spinner.show();
    this.tierService.getTraffic().subscribe({
      next: data => {
        this.result = data.IP_Address;
        this.spinner.hide();
        this.isBestResult = true;
      },
      error: error => {
        this.spinner.hide();
        console.log(error);
        this.toastr.error(error.error.detail);
      }
    });

  }

  clearData() {
    this.selectedItems = [];
    this.isBestResult = false;
  }

}
