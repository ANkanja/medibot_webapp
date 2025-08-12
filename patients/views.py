from django.shortcuts import render
from . models import Patient
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PatientForm, VisitForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

def all_patients(request):
    patients = Patient.objects.all()
    return render(request, 'all_patients.html', {'patients': patients})

def new_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientForm()
    return render(request, 'new_patient.html', {'form': form})

def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'edit_patient.html', {'form': form, 'patient': patient})

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        patient.delete()
        return redirect('all_patients')
    return render(request, 'delete_patient.html', {'patient': patient})

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'patient_detail.html', {'patient': patient})

def new_diagnosis(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = patient
            visit.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = VisitForm()
    return render(request, 'new_diagnosis.html', {'form': form, 'patient': patient})

def visit_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    visits = patient.visits.all()
    return render(request, 'visit_history.html', {'patient': patient, 'visits': visits})

