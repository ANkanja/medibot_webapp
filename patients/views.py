from django.shortcuts import render, get_object_or_404, redirect
from . models import Patient, LearningMaterial, Referrals, CHPProfile
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PatientForm, VisitForm, ReferralForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

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



def training(request):
    materials = LearningMaterial.objects.all()
    return render(request, 'training.html', {'materials': materials})


def all_referrals(request):
    if request.user.is_superuser:  
        # admins see all referrals
        referrals = Referrals.objects.all().order_by('-created_at')
    else:
        try:
            chp_profile = request.user.chpprofile
            referrals = Referrals.objects.filter(chp=chp_profile).order_by('-created_at')
        except AttributeError:  
            # user has no CHP profile → deny access or redirect
            return redirect('signup')  # or show error message
    return render(request, 'all_referrals.html', {'referrals': referrals})


def new_referral(request):
    if request.method == "POST":
        form = ReferralForm(request.POST)
        if form.is_valid():
            referral = form.save(commit=False)
            referral.chp = request.user
            referral.save()
            return redirect("referrals_dashboard")
    else:
        form = ReferralForm()
    return render(request, "new_referral.html", {"form": form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check if the user exists
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in successfully!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
        
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out. Thanks for stopping by!")
    return redirect('index')
    

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Authenticate the user(Log in the user)
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('index')
        else:
            messages.error(request, "Registration failed. Please try again.")
            return redirect('signup') 
    else:
        return render(request, 'signup.html', {'form': form})


