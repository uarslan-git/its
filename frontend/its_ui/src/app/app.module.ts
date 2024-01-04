import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { MarkdownModule, MarkedOptions } from 'ngx-markdown';
import { DatePipe } from '@angular/common';

import { CodePanelComponent } from './code-panel/code-panel.component';

import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { SharedModule } from './shared/shared.module';

import { HttpClientModule } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { TaskPanelComponent } from './task-panel/task-panel.component';
import { NavigationBarComponent } from './navigation-bar/navigation-bar.component';
import { FeedbackPanelComponent } from './feedback-panel/feedback-panel.component';
import { ActionPanelComponent } from './code-panel/action-panel/action-panel.component';
import { CodeEditorComponent } from './code-panel/code-editor/code-editor.component';
import { MultipleChoiceComponent } from './code-panel/multiple-choice/multiple-choice.component';
import { AuthComponent } from './auth/auth.component';
import { ProfileComponent } from './profile/profile.component';

@NgModule({
  declarations: [
    AppComponent,
    CodePanelComponent,
    TaskPanelComponent,
    NavigationBarComponent,
    FeedbackPanelComponent,
    ActionPanelComponent,
    CodeEditorComponent,
    MultipleChoiceComponent,
    AuthComponent,
    ProfileComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    ReactiveFormsModule,
    SharedModule,
    MatButtonModule,
    MatCheckboxModule,
    MarkdownModule.forRoot({
      markedOptions: {
        provide: MarkedOptions,
        useValue: {
          gfm: false
        },
      },
    }),
  ],
  providers: [DatePipe],
  bootstrap: [AppComponent]
})
export class AppModule { }
