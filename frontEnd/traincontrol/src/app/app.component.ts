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
    this.commandService.postCommand("start", this.direction)
  }

  onFaster() {
    // console.info("onFaster")
    this.commandService.postCommand("faster", this.direction)
  }

  onSlower() {
    // console.info("onSlower")
    this.commandService.postCommand("slower", this.direction)
  }

  onStop() {
    // console.info("onStop")
    this.commandService.postCommand("stop", this.direction)
  }
}
