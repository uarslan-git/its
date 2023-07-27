import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';

import { CodeEditorComponent } from './code-editor/code-editor.component';

import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { SharedModule } from './shared/shared.module';

import { HttpClientModule } from '@angular/common/http';
import {MatButtonModule} from '@angular/material/button';
import { TaskPanelComponent } from './task-panel/task-panel.component';


@NgModule({
  declarations: [
    AppComponent,
    CodeEditorComponent,
    TaskPanelComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    ReactiveFormsModule,
    SharedModule,
    MatButtonModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
