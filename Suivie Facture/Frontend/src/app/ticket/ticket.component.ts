import { TicketService } from '../../services/ticket.service';
import { Component, OnInit } from '@angular/core';
import { CollapseService } from '../../services/collapse.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-ticket',
  templateUrl: './ticket.component.html',
  styleUrl: './ticket.component.css'
})
export class TicketComponent implements OnInit {
  tikets: any[] = [];
  selectedTicket: any | null = null;
  Of_num: string = '';

  constructor(
    private router: Router,
    public collapseService: CollapseService,
    private ticketService: TicketService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.Of_num = params['OF_num'];
      if (this.Of_num) {
        this.fetchTicket();
      } else {
        console.error('Of_num is missing from queryParams');
      }
    });
  }

  async fetchTicket(): Promise<void> {
    if (this.Of_num && this.Of_num.length > 0) {
      try {
        const data = await this.ticketService.getTickets(this.Of_num);
        this.tikets = data.OFS || [];
      } catch (error) {
        console.error('Error fetching OFs:', error);
      }
    }
  }
  onImageError(event: Event) {
    (event.target as HTMLImageElement).src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" height="48" viewBox="0 96 960 960" width="48"><path fill="gray" d="M256 976q-33 0-56.5-23.5T176 896V336q0-33 23.5-56.5T256 256h448q33 0 56.5 23.5T784 336v560q0 33-23.5 56.5T704 976H256Zm224-290q31 0 52.5-21.5T554 612q0-31-21.5-52.5T480 538q-31 0-52.5 21.5T406 612q0 31 21.5 52.5T480 686Zm-224 178h448V801L624 625l-80 106-96-144-144 194v83Zm0-632v560-560Z"/></svg>';
  }
  
  

  toggleMenu() {

    this.collapseService.toggleCollapse();
  }
}
