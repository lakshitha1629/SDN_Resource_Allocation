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

  dataSearchFn(term: string, item: any) {
    term = term.toLowerCase();
    let splitTerm = term.split(' ').filter(t => t);
    let isWordThere: any = [];
    splitTerm.forEach(arr_term => {
      let search = item['userFullAll'].toLowerCase();
      isWordThere.push(search.indexOf(arr_term) != -1);
    });
    const all_words = (this_word: any) => this_word;

    return isWordThere.every(all_words);
  }

  clearModel() {
    this.selectedItems = [];
  }


  calculateMax() {
    let total = 0;
    this.selectedItems.forEach(item => {
      item['total'] = item.vCPUs * 2 + item.NetworkBandwidth + item.RAM;
    });

    // get max total object in this.selectedItems
    let max_total = Math.max.apply(null, this.selectedItems.map(function (obj) {
      return obj.total;
    }));

    // get max tier object in this.selectedItems
    let max_tier = this.selectedItems.find(obj => {
      return obj.total == max_total;
    });

    return max_tier;
  }

  selectBestIP() {
    this.tierData = this.calculateMax();
    this.isBestResult = true;
  }

  clearData() {
    this.selectedItems = [];
    this.isBestResult = false;
  }

}
