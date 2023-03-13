from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'password', 'mobile', 'aadhar_number', 'email_otp', 'email_verification',
                    'mobile_otp', 'mobile_verification', 'aadhar_verification', 'verified_user', 'verified_user_id_proof']


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile_image', 'username', 'email', 'mobile',
                    'aadhar_number', 'name', 'DOB', 'gender', 'kyc_status', 'is_verifed_user']


@admin.register(LoggedInData)
class LoggedInDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'session']


@admin.register(AadharData)
class AaadharAdmin(admin.ModelAdmin):
    list_display = ['id', 'serial', 'card_number', 'VID',
                    'profile', 'name', 'DOB', 'gender', 'address', 'mobile']


@admin.register(FIRData)
class FIRDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'serial', 'fir_id', 'profile', 'name',
                    'father_name', 'address', 'phone_number', 'fir_type']


@admin.register(ExtractFacesData)
class ExtractFacesDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'serial', 'from_database']


@admin.register(CascadeAndTrainerData)
class CascadeAndTrainerDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'file_name']


@admin.register(TrainedDataSet)
class TrainedDataSetAdmin(admin.ModelAdmin):
    list_display = ['id', 'serial', 'name', 'aadhar_number']


@admin.register(TrackingUserData)
class TrackingUserDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'case_id', 'username', 'user_profile', 'case_name',
                    'police_station_id', 'time_at_droped', 'date_at_droped', 'tracking_progress']


@admin.register(PoliceStationData)
class PoliceStationDataAdmin(admin.ModelAdmin):
    list_display = ['station_id', 'address', 'phone', 'email']
