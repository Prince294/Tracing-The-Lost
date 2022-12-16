from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','username','password','mobile','aadhar_number','email_otp','email_verification','mobile_otp','mobile_verification','aadhar_verification','verified_user','verified_user_id_proof']
    
@admin.register(LoggedInData)
class LoggedInDataAdmin(admin.ModelAdmin):
    list_display = ['id','username','session']
    
@admin.register(AadharData)
class LoggedInDataAdmin(admin.ModelAdmin):
    list_display = ['id','serial','card_number','VID','profile','name','DOB', 'gender','address']

@admin.register(FIRData)
class LoggedInDataAdmin(admin.ModelAdmin):
    list_display = ['id','serial','fir_id','profile','name','father_name','address','phone_number','fir_type']
    
@admin.register(TrainigImagesData)
class LoggedInDataAdmin(admin.ModelAdmin):
    list_display = ['id','image','serial','from_database']
    
@admin.register(CascadeAndTrainerData)
class LoggedInDataAdmin(admin.ModelAdmin):
    list_display = ['id','name','file_name']
    
@admin.register(TrainedDataSet)
class LoggedInDataAdmin(admin.ModelAdmin):
    list_display = ['id','serial','name','aadhar_number']
    

@admin.register(TrackingUserData)
class TrackingUserDataAdmin(admin.ModelAdmin):
    list_display = ['id','username','profile','name','police_station_droped','time_at_droped','date_at_droped','tracking_progress']
    

@admin.register(AllUsersTrackingData)
class AllUsersTrackingData(admin.ModelAdmin):
    list_display = ['id','uid','from_database','database_serial']