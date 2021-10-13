import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'angular';
  form: FormGroup;

  constructor(private fb: FormBuilder, private apiService: ApiService) {
    this.form = this.fb.group({
      email: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  login_with_credentials(value: any) {
    let email = value.email;
    let password = value.password;
    this.apiService.login(email, password).subscribe((data) => {
      if (data.login) {
        console.log();
        alert('Has iniciado sesión a EDD');
      }
    });
  }
}
