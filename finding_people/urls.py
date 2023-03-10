from django.urls import path
from . import views

urlpatterns = [
########################################################### admin urls ###############################################################
    path('adm/save_aadhar', views.AadharDetail,name="AadharDetail"),
    path('adm/save_fir', views.FIRDataSaver,name="FIRData"),
    path('adm/save_police_station', views.PoliceStationDataFunction,name="PoliceStation"),
    
    path('adm/extract_faces', views.ExtractFaces,name="ExtractFaces"),
    path('adm/trainimages', views.TrainImageAndSave,name="trainImages"),
    path('adm/cascadeandtrainer',views.CascadeFileAndTrainer,name="cascadeFileAndTrainer"),
    
########################################################## verification ##############################################################
    path('police/verification/<str:case_id>', views.SuspectArrivePoliceStation,name="SuspectArrivePoliceStation"),
    
    
############################################################ user urls ###############################################################
    path('', views.home,name="home"),
    path('user', views.UserView,name="userView"),
    path('user/verification', views.VerifyUser,name="userVerification"),
    
    path('user/login', views.UserLogin,name="userLogin"),
    path('user/logout', views.UserLogout,name="userLogout"),
    path('user/face/recognize', views.FaceRecognize,name="faceRecognize"),
]