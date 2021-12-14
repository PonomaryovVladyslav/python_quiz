import {Component} from '@angular/core';
import {ActivatedRoute, NavigationEnd, Router} from "@angular/router";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent{
  token: string | null | undefined;
  current_url: string;
  constructor(private route: ActivatedRoute, private router:Router) {
    this.current_url = router.url;
    router.events.subscribe((val) => this.check_auth(val))
  }
  check_auth(val:any): void{
    if (val instanceof NavigationEnd){
      this.current_url = val.url;
      this.token = localStorage.getItem('token');
      if ((this.token === null) && (val.url != '/login')){
        this.router.navigate(['login'])
      }
    }
  }
}
