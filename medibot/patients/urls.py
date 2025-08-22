from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all_patients/', views.all_patients, name='all_patients'),
    path('new_patient/', views.new_patient, name='new_patient'),
    path('edit_patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('patient_detail/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('new_diagnosis/<int:patient_id>/', views.new_diagnosis, name='new_diagnosis'),
    path('visit_history/<int:patient_id>/', views.visit_history, name='visit_history'),
    path('training/', views.training, name='training'),
]