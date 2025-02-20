import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../api.service';
import { Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { PlanModalComponent } from '../plan-modal/plan-modal.component';
import { StudyPlan } from '../../../shared/interfaces/study-plan.interface';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faCirclePlus } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-plan-page',
  standalone: true,
  imports: [
    CommonModule,
    FontAwesomeModule,
  ],
  templateUrl: './plan-page.component.html',
  styleUrl: './plan-page.component.css'
})
export class PlanPageComponent implements OnInit {
  faCirclePlus = faCirclePlus;
  studyPlans: StudyPlan[] = []; // Variável para armazenar os dados retornados

  constructor(private apiService: ApiService,
    private router: Router,
    public dialog: MatDialog
  ) { }

  ngOnInit() {
    this.fetchStudyPlans();
  }

  public openLoginModal(): void {
    this.dialog.open(
      PlanModalComponent
    ).afterClosed().subscribe();
  }

  studyPlanData = {
    name: 'New Study Plan',
    description: 'Description of the new study plan'
  };

  openStudyPlanModal() {
    const dialogRef = this.dialog.open(PlanModalComponent);

    dialogRef.afterClosed().subscribe((newPlan) => {
      if (newPlan) {
        this.studyPlans.push(newPlan); // Adicione o novo tópico à lista
      }
    });
  }

  fetchStudyPlans() {
    this.studyPlans = [];
    this.apiService.getAllStudyPlans().subscribe(
      (data) => {
        console.log('Dados recebidos:', data);
        this.studyPlans = data; // Armazena os dados retornados
      },
      (error) => {
        console.error('Erro ao buscar study plans:', error);
      }
    );
  }

  executePlan(id: number | undefined) {
    if (!id) {
      return;
    }
    this.router.navigate([`/planos/${id}/executar`]);
  }

  editPlan(id: number | undefined) {
    if (!id) {
      return;
    }
    this.router.navigate([`/planos/${id}`]);
  }

}
