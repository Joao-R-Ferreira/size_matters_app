import { bootstrapApplication } from '@angular/platform-browser';
import { MainComponent } from './app/main/main';

bootstrapApplication(MainComponent)
  .catch(err => console.error(err));

//old main.ts
// import { bootstrapApplication } from '@angular/platform-browser';
// import { appConfig } from './app/app.config';
// import { App } from './app/app';

// bootstrapApplication(App, appConfig)
//   .catch((err) => console.error(err));
