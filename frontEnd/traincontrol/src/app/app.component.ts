import {Component} from '@angular/core';
import {PostcommandService} from 'src/services/postcommand.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'traincontrol';
  commandService : PostcommandService;
  direction : string = "forward";

  constructor(private _commandService: PostcommandService) {
    this.commandService = _commandService;
  }

  onStart() {
    this.commandService.postCommand("start", this.direction)
  }

  onFaster() {
    this.commandService.postCommand("faster", this.direction)
  }

  onSlower() {
    this.commandService.postCommand("slower", this.direction)
  }

  onStop() {
    this.commandService.postCommand("stop", this.direction)
  }
}
