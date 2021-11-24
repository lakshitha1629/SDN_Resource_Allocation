import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { MonitorComponent } from './features/monitor/monitor.component';
import { PredictTierComponent } from './features/predict-tier/predict-tier.component';
import { TiersListComponent } from './features/tiers-list/tiers-list.component';
import { TrafficLogComponent } from './features/traffic-log/traffic-log.component';
import { LayoutComponent } from './layout/layout.component';

const routes: Routes = [
  { path: '', redirectTo: 'main', pathMatch: 'full' },
  {
    path: 'main',
    component: LayoutComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      {
        path: 'dashboard',
        component: DashboardComponent,
      }, {
        path: 'tiers-list',
        component: TiersListComponent,
      }, {
        path: 'predict-tier',
        component: PredictTierComponent,
      }, {
        path: 'monitor',
        component: MonitorComponent,
      }, {
        path: 'traffic-log',
        component: TrafficLogComponent,
      }
    ],
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {

}
