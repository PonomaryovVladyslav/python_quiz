import {Component, Input, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent implements OnInit, OnChanges {
  username: string | null = localStorage.getItem('username');
  @Input() current_url: string | undefined;

  constructor(private route: ActivatedRoute, private router: Router) {
  }

  ngOnInit(): void {
  }


  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    this.router.navigate(['login']);
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.current_url = this.router.url;
  }
}
