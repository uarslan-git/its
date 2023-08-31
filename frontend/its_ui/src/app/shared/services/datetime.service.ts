import { Injectable } from '@angular/core';
import { DatePipe } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class DatetimeService {

  constructor(public datePipe: DatePipe) { }

  datetimeNow() {
    const datetime_obj = {
      "local": this.datePipe.transform((new Date), 'dd.MM.yyyy HH:mm:ss'),
      "utc": this.datePipe.transform((new Date), 'dd.MM.yyyy HH:mm:ss', '+0:00'),
    };
    return datetime_obj
  }
}
