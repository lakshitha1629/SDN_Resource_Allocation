import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastrService } from 'ngx-toastr';
import { interval } from 'rxjs';
import { TierService } from 'src/app/core/service/tier.service';

@Component({
  selector: 'app-traffic-log',
  templateUrl: './traffic-log.component.html',
  styleUrls: ['./traffic-log.component.scss']
})
export class TrafficLogComponent implements OnInit {
  myDate = new Date();
  dataList: any = [];
  isResult: boolean = false;
  resultImg: any;

  formGroup: FormGroup = new FormGroup({
    year: new FormControl('', [Validators.required])
  });

  constructor(
    private toastr: ToastrService,
    private spinner: NgxSpinnerService,
    private tierService: TierService) { }

  ngOnInit(): void {
  }

  ngAfterViewInit() {
    let count: number = 0;
    interval(10 * 1000).subscribe(val => {
      count = count + 1;
      this.getPredictTrafficAfter(count);
    });

  }

  getPredictTrafficAfter(count: number) {
    this.tierService.getPredictTraffic().subscribe({
      next: data => {
        const list = data;
        this.dataList = list.slice(0, count);
      },
      error: error => {
        console.log(error);
        this.toastr.error(error.error.detail);
      }
    });
  }

  onSubmit() {
    const data = {
      year: parseInt(this.formGroup.controls.year.value)
    }
    this.spinner.show();
    this.tierService.getFutureTraffic(data).subscribe({
      next: data => {
        console.log(data.OutputValue);
        this.resultImg = data.Img;
        this.isResult = true;
        this.spinner.hide();
        this.formGroup.reset();
        this.toastr.success('Successfully Prediction');
      },
      error: error => {
        this.spinner.hide();
        this.formGroup.reset();
        console.log(error);
        this.toastr.error(error.error.detail);
      }
    });

  }

  clearData() {
    this.isResult = false;
    this.formGroup.reset();
  }

}
function mergeMap(arg0: () => any): import("rxjs").OperatorFunction<number, unknown> {
  throw new Error('Function not implemented.');
}

