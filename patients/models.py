from django.db import models

# Create your models here.



# Category of patients
# This model can be used to categorize patients based on their conditions or other criteria based on demographica or conditions
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'


# Patient model
class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    full_name = models.CharField(max_length=100, blank=False)
    date_of_birth = models.DateField(null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)
    phone_number = models.CharField(max_length=15, blank=False)
    village = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    
# This model tracks the last visit date of the patient and all patient data from the visit
class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically update last_visit on the patient
        self.patient.last_visit = self.date
        self.patient.save()


# This model is for the education sector
class LearningCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class LearningMaterial(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('video', 'Video'),
        ('document', 'Document'),
        ('link', 'External Link'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES)
    video_file = models.FileField(upload_to='learning/videos/', blank=True, null=True)
    document_file = models.FileField(upload_to='learning/documents/', blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)
    category = models.ForeignKey('LearningCategory', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LearningProgress(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    material = models.ForeignKey(LearningMaterial, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.material.title}"


