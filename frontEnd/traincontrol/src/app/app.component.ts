import {Component} from '@angular/core';
import {PostcommandService} from 'src/services/postcommand.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'train control';
  commandService : PostcommandService;
  direction : string = "forward";

  constructor(private _commandService: PostcommandService) {
    console.info("Starting")
    this.commandService = _commandService;
  }

  onStart() {
    // console.info("onStart")
    // this.commandService.postCommand("start", this.direction)
    this.commandService.postStart().subscribe(data => data);
  }

  onFaster() {
    // console.info("onFaster")
    // this.commandService.postCommand("faster", this.direction)
    this.commandService.postFaster().subscribe(data => data);
  }

  onSlower() {
    // console.info("onSlower")
    // this.commandService.postCommand("slower", this.direction)
    this.commandService.postSlower().subscribe(data => data);
  }

  onStop() {
    // console.info("onStop")
    // this.commandService.postCommand("stop", this.direction)
    this.commandService.postStop().subscribe(data => data);
  }
}
