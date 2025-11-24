import { Component, ElementRef, EventEmitter, OnInit, Output } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ValidatorFn, AbstractControl } from '@angular/forms';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { User } from 'src/app/models/user';
import { AccommodationService } from 'src/app/services/accommodation.service';
import { UserService } from 'src/app/services/user.service';

declare var bootstrap: any;
@Component({
  selector: 'app-accomodation-registration-form',
  templateUrl: './accomodation-registration-form.component.html',
  styleUrls: ['./accomodation-registration-form.component.css']
})
export class AccomodationRegistrationFormComponent implements OnInit {

  @Output() accommodationAdded = new EventEmitter<void>();

 currentUserId!: number; 
  accommodationForm!: FormGroup;
  submitted = false;
  errorMessage: string | null = null;
  user!: User;

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private accommodationService: AccommodationService,
    private elementRef: ElementRef
  ) { }

  ngOnInit(): void {
    this.accommodationForm = this.fb.group({
      name: ['', Validators.required],
      ntak: ['', Validators.required],
      vendegemId:[''],
      vendegemRef:[''],
    });
    this.route.paramMap.subscribe((params: ParamMap) => {
      console.log(params)
    
    });
  }

  get form() { return this.accommodationForm.controls; }

  onSubmit(): void {
    this.submitted = true;
    if (this.accommodationForm.invalid) {
      return;
    }

    const { name, vendegemId, vendegemRef, ntak } = this.accommodationForm.value;
    const creationRequest = {
      name: name,
      user_id:2,
      vendegemId: vendegemId,
      ntak_no: ntak,
      vendegemRef: vendegemRef
    };
    console.log("REG")
      console.log(this.user)
    this.accommodationService.registerNewAccommodation(creationRequest).subscribe({
      next: success => {
        console.log("success")
        if (success) {
          this.resetForm();
          this.accommodationAdded.emit();
        }
        this.closeModal();
      },
      error: error => {
        console.error('Hiba a regisztráció során:', error);
        this.errorMessage = `Hiba: ${error.error.detail}`;
      }
    });
  }

  closeModal() {
    const modalEl = this.elementRef.nativeElement.closest('.modal');
    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    modalInstance.hide();
  }

  resetForm(): void {
    this.errorMessage = null;
    this.submitted = false;
    this.accommodationForm.reset();
  }
}