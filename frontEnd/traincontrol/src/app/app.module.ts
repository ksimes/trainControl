import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {FormsModule} from "@angular/forms";
import {PostcommandService} from "../services/postcommand.service";
import {HttpClient} from "@angular/common/http";

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClient,
  ],
  providers: [PostcommandService],
  bootstrap: [AppComponent]
})
export class AppModule { }
