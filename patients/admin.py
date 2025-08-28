from django.contrib import admin
from .models import Patient, LearningCategory, LearningMaterial

# Register your models here.
admin.site.register(Patient)

# Optional: customize admin display
@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'material_type', 'category', 'created_at')
    list_filter = ('material_type', 'category')
    search_fields = ('title', 'description')

@admin.register(LearningCategory)
class LearningCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# CHPProfile
class CHPProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "region", "facility_assigned")


# Show referrals in admin
class ReferralsAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "facility", "referral_type", "created_at", "chp")
    list_filter = ("referral_type", "created_at", "chp")
    search_fields = ("patient_name", "facility", "notes")
