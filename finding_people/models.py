from datetime import datetime
from django.utils import timezone
from django.db import models
from django.utils.deconstruct import deconstructible
from pathlib import Path
import os


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):

        self.path = 'staticFiles\\'+sub_path
        self.signature = 0

    def __call__(self, instance, filename):

        dir = os.path.join(Path(__file__).parent.parent, self.path)
        if not os.path.exists(dir):
            os.makedirs(dir)

        count = 0
        for paths in os.listdir(os.path.join(Path(__file__).parent.parent, self.path)):
            count += 1

        try:
            if instance.from_database and instance.from_database == 'aadhar':
                self.signature = 1
            elif instance.from_database and instance.from_database == 'fir':
                self.signature = 2

            counter = 0
            searchStr = str(self.signature)+"-" + str(instance.serial)
            for paths in os.listdir(os.path.join(Path(__file__).parent.parent, self.path)):
                if paths.startswith(searchStr):
                    counter += 1

            name = str(self.signature)+"-" + \
                str(instance.serial) + "-"+str(counter+1)

            ext = filename.split('.')[-1]
            filename = '{}.{}'.format(name, ext)
            return os.path.join(self.path, filename)
        except:
            name = str(count+1)
            ext = filename.split('.')[-1]
            filename = '{}.{}'.format(name, ext)
            return os.path.join(self.path, filename)


# Create your models here.

path_and_id_proof = PathAndRename('User Verfication ID Proof')


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    # user_profile = models.ImageField(max_length=100,unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    mobile = models.BigIntegerField(unique=True, null=True)
    aadhar_number = models.BigIntegerField(unique=True, null=True)
    email_otp = models.IntegerField(blank=True, null=True)
    email_verification = models.BooleanField(default=False)
    mobile_otp = models.IntegerField(blank=True, null=True)
    mobile_verification = models.BooleanField(default=False)
    aadhar_verification = models.BooleanField(default=False)
    verified_user = models.BooleanField(default=False)
    verified_user_id_proof = models.ImageField(
        blank=True, upload_to=path_and_id_proof)


class LoggedInData(models.Model):
    session = models.CharField(max_length=50, unique=True, blank=True)
    username = models.CharField(max_length=100, unique=True)


class UserDetails(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    mobile = models.BigIntegerField(unique=True, null=True)
    aadhar_number = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=50)
    DOB = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)


@deconstructible
class Serial_Generator(object):
    def __init__(self, sub_path):
        self.path = 'static\\'+sub_path

    def __call__(self):
        count = 0
        try:
            for paths in os.listdir(os.path.join(Path(__file__).parent.parent, self.path)):
                count += 1
        except:
            count = 0
        name = str(count+1)
        return name


aadharSerial = Serial_Generator('Aadhar Data')
path_and_rename_aadhar = PathAndRename('Aadhar Data')


class AadharData(models.Model):
    card_number = models.BigIntegerField(unique=True)
    serial = models.IntegerField(unique=True, default=aadharSerial)
    VID = models.BigIntegerField(unique=True)
    profile = models.ImageField(upload_to=path_and_rename_aadhar)
    name = models.CharField(max_length=50)
    DOB = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    mobile = models.BigIntegerField(unique=True, null=True)


path_and_rename_fir = PathAndRename('FIR Data')
firSerial = Serial_Generator('FIR Data')


class FIRData(models.Model):
    fir_id = models.BigIntegerField(unique=True)
    serial = models.IntegerField(unique=True, default=firSerial)
    profile = models.ImageField(upload_to=path_and_rename_fir)
    name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    fir_type = models.CharField(max_length=50)


path_and_rename_training = PathAndRename('TrainingImage')


class ExtractFacesData(models.Model):
    serial = models.BigIntegerField(blank=False)
    from_database = models.CharField(max_length=50, default='None')
    image = models.ImageField(upload_to=path_and_rename_training, blank=True)


class CascadeAndTrainerData(models.Model):
    name = models.CharField(max_length=50)
    file_name = models.FileField(upload_to='CascadeAndTrainer')

    def delete(self, using=None, keep_parents=False):
        self.file_name.storage.delete(self.file_name.name)
        super().delete()


class TrainedDataSet(models.Model):
    serial = models.BigIntegerField(unique=True, blank=False)
    name = models.CharField(max_length=100)
    aadhar_number = models.BigIntegerField(unique=True)


path_and_rename_tracking = PathAndRename('TrackingImage')


class TrackingUserData(models.Model):
    case_id = models.BigIntegerField(unique=True, null=True)
    username = models.CharField(max_length=50)
    user_profile = models.ImageField(upload_to=path_and_rename_tracking)
    case_name = models.CharField(max_length=50, default='Unknown')
    police_station_id = models.CharField(max_length=200, null=True)
    time_at_droped = models.TimeField(default=datetime.now().time())
    date_at_droped = models.DateField(default=timezone.now)
    tracking_progress = models.CharField(max_length=20, default='Pending')


class PoliceStationData(models.Model):
    station_id = models.AutoField(unique=True, primary_key=True, default=None)
    address = models.CharField(max_length=200)
    phone = models.BigIntegerField(unique=True)
    email = models.EmailField(unique=True, null=True)
