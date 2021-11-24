import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastrService } from 'ngx-toastr';
import { TierService } from 'src/app/core/service/tier.service';

@Component({
  selector: 'app-predict-tier',
  templateUrl: './predict-tier.component.html',
  styleUrls: ['./predict-tier.component.scss']
})
export class PredictTierComponent implements OnInit {
  isPredictionResult: boolean = false;
  predictionResult: string | undefined;

  formGroup: FormGroup = new FormGroup({
    networkBandwidth: new FormControl('', [Validators.required]),
    userType: new FormControl('', [Validators.required]),
    processorSpeed: new FormControl('', [Validators.required]),
    ram: new FormControl('', [Validators.required]),
    vCPUs: new FormControl('', [Validators.required])
  });

  constructor(
    private toastr: ToastrService,
    private spinner: NgxSpinnerService,
    private tierService: TierService) { }

  ngOnInit(): void {
  }

  onSubmit() {
    const predictData =
    {
      NetworkBandwidth: [parseInt(this.formGroup.controls.networkBandwidth.value)],
      UserType: [parseInt(this.formGroup.controls.userType.value)],
      ProcessorSpeed: [parseInt(this.formGroup.controls.processorSpeed.value)],
      RAM: [parseInt(this.formGroup.controls.ram.value)],
      vCPUs: [parseInt(this.formGroup.controls.vCPUs.value)]
    }
    this.spinner.show();
    this.tierService.getSuggestion(predictData).subscribe({
      next: data => {
        console.log(data.OutputValue);
        this.predictionResult = data.OutputValue;
        this.isPredictionResult = true;
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
    this.isPredictionResult = false;
    this.predictionResult = undefined;
  }

  createTier() {
    this.spinner.show();
    this.tierService.createTier(1).subscribe({
      next: data => {
        console.log(data);
        this.spinner.hide();
      },
      error: error => {
        this.spinner.hide();
        console.log(error);
      }
    });

  }
}
