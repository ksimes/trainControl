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
  public StartApiUrl:string = "start.php";
  public FasterApiUrl:string = "faster.php";
  public SlowerApiUrl:string = "slower.php";
  public StopApiUrl:string = "stop.php";

  constructor(private _http: HttpClient)  {
  }

  public postCommand(command: string, direction: string): void {
    let body = { action: command, direction: direction };
    console.info("URL: " + this.Server + "/" + this.BaseApiUrl);
    console.info("body: " + body);
    this._http.post(this.Server + "/" + this.BaseApiUrl, body);
  }

  private poster(url : string): Observable<void> {
    console.info("URL: " + url);
    return this._http.get<void>(url);
  }

  public postStart(): Observable<void> {
    let url = this.Server + "/" + this.StartApiUrl
    return this.poster(url);
  }

  public postFaster(): Observable<void> {
    let url = this.Server + "/" + this.FasterApiUrl
    return this.poster(url);
  }

  public postSlower(): Observable<void> {
    let url = this.Server + "/" + this.SlowerApiUrl
    return this.poster(url);
  }

  public postStop(): Observable<void> {
    let url = this.Server + "/" + this.StopApiUrl
    return this.poster(url);
  }
}
