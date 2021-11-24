import { BrowserModule } from '@angular/platform-browser';
import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AkitaNgDevtools } from '@datorama/akita-ngdevtools';
import { AkitaNgRouterStoreModule } from '@datorama/akita-ng-router-store';
import { environment } from '../environments/environment';
import { FooterComponent } from './layout/footer/footer.component';
import { SideBarComponent } from './layout/side-bar/side-bar.component';
import { TopBarComponent } from './layout/top-bar/top-bar.component';
import { LayoutComponent } from './layout/layout.component';
import { NgBootstrapFormValidationModule } from 'ng-bootstrap-form-validation';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { NgxSpinnerModule } from "ngx-spinner";
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { TiersListComponent } from './features/tiers-list/tiers-list.component';
import { PredictTierComponent } from './features/predict-tier/predict-tier.component';
import { CommonModule } from '@angular/common';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrModule } from 'ngx-toastr';
import { NgSelectModule } from '@ng-select/ng-select';
import { MonitorComponent } from './features/monitor/monitor.component';
import { TrafficLogComponent } from './features/traffic-log/traffic-log.component';

@NgModule({
  declarations: [
    AppComponent,
    FooterComponent,
    SideBarComponent,
    TopBarComponent,
    LayoutComponent,
    DashboardComponent,
    TiersListComponent,
    PredictTierComponent,
    MonitorComponent,
    TrafficLogComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    HttpClientModule,
    environment.production ? [] : AkitaNgDevtools.forRoot(),
    AkitaNgRouterStoreModule,
    NgSelectModule,
    FormsModule,
    ReactiveFormsModule,
    NgBootstrapFormValidationModule.forRoot(),
    CommonModule,
    NgxSpinnerModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot({
      timeOut: 4000,
      positionClass: 'toast-top-center'
    })
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
