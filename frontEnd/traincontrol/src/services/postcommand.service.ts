import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class PostcommandService {
  // public Host:string = window.location.hostname;
  // public Port:string = window.location.port;
  public Host:string = "simonking.website";
  public Port:string = "80";
  public Server:string = "http://" + this.Host + ":" + this.Port;

  // public BaseApiUrl:string = "/api";
  public BaseApiUrl:string = "publish.php";

  constructor(private _http: HttpClient)  { }

  public postCommand(command: string, direction: string): void {
    let body = { action: command, direction: direction };
    this._http.post(this.Server + this.BaseApiUrl, body);
  }
}
