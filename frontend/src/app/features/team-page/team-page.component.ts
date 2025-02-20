import { CommonModule } from '@angular/common';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faGithub, faLinkedin } from '@fortawesome/free-brands-svg-icons';
import { Component } from '@angular/core';

@Component({
    selector: 'app-team-page',
    standalone: true,
    imports: [
      CommonModule,
      FontAwesomeModule,
    ],
    templateUrl: './team-page.component.html',
    styleUrl: './team-page.component.css',
})

export class TeamPageComponent {
  public faGithub = faGithub;
  public faLinkedin = faLinkedin;
  teamMembers = [
    {
      name: 'Henrique Parede',
      description: 'Um apreciador de café, Star Wars e dormir tarde',
      avatar: '../../../../assets/fotohenrique.png',
      github: 'https://github.com/Henrique-hpds',
      linkedin: 'https://l1nk.dev/xYz0Z'
    },
    {
      name: 'Maria B. Moreira',
      description: 'Cinéfila, amante de livros e esfomeada',
      avatar: '../../../../assets/fotomabe.jpeg',
      github: 'https://github.com/mabemoreira',
      linkedin: 'https://l1nk.dev/7whU7'
    },

    {
      name: 'Pedro Brasil',
      description: 'Um fã de jogar durante as aulas',
      avatar: '../../../../assets/fotopedro.png',
      github: 'https://github.com/PedroBrasil111',
      linkedin: 'https://acesse.one/jj7p4'
    },

    {
      name: 'T. H. de Camargo',
      description: 'Ama cachorros',
      avatar: '../../../../assets/fotothiago.jpeg',
      github: 'https://github.com/THdeCamargoJ',
      linkedin: 'https://l1nk.dev/rCK6C'
    },

    {
      name: 'Raphael Salles',
      description: 'Tem uma apreciação única por banhos',
      avatar: '../../../../assets/fotorapha.jpeg',
      github: 'https://github.com/RaphaelSVSouza',
      linkedin: 'https://www.linkedin.com/in/raphael-sv-souza/'
    }
  ];
}

