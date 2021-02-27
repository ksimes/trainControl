import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class PostcommandService {
  // public Host:string = window.location.hostname;
  // public Port:string = window.location.port;
  public Host:string = "simonking.website";
  public Port:string = "80";
  public Server:string = "http://" + this.Host; // + ":" + this.Port;

  // public BaseApiUrl:string = "/api";
  public BaseApiUrl:string = "publish.php";

  constructor(private _http: HttpClient)  {
  }

  public postCommand(command: string, direction: string): Observable<void> {
    let url = this.Server + "/" + this.BaseApiUrl
    let body = { action: command, direction: direction };
    return this._http.post<void>(url, body);
  }
}
