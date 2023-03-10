from rest_framework import serializers
from .models import User, UserDetails, LoggedInData, AadharData, FIRData, ExtractFacesData, CascadeAndTrainerData, TrainedDataSet, TrackingUserData, PoliceStationData
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'mobile', 'aadhar_number', 'email_otp', 'email_verification',
                  'mobile_otp', 'mobile_verification', 'aadhar_verification', 'verified_user', 'verified_user_id_proof']

    # validations
    def validate_password(self, value):
        special_char = '[@_!$%^&*()<>?/\|}{~:]#'

        isNum = any(i.isdigit() for i in value)
        isUpper = any(i.isupper() for i in value)
        isLower = any(i.islower() for i in value)
        isSpecial = any(
            special_char[i] in value for i in range(len(special_char)))

        if not isNum or not isUpper or not isLower or len(value) < 10 or not isSpecial:
            raise serializers.ValidationError(
                'Please Maintain Password Criteria')
        value = make_password(value)
        return value

    def validate_username(self, value):
        value = value.lower()
        return value

    def validate_email(self, value):
        value = value.lower()
        return value

    def validate_mobile(self, value):
        value = int(value)
        return value


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id', 'username', 'email', 'mobile',
                  'aadhar_number', 'name', 'DOB', 'gender']

    def validate_username(self, value):
        value = value.lower()
        return value

    def validate_email(self, value):
        value = value.lower()
        return value

    def validate_mobile(self, value):
        value = int(value)
        return value


class LoggedInDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoggedInData
        fields = ['id', 'username', 'session']

    def validate_password(self, value):
        special_char = '[@_!$%^&*()<>?/\|}{~:]#'

        isNum = any(i.isdigit() for i in value)
        isUpper = any(i.isupper() for i in value)
        isLower = any(i.islower() for i in value)
        isSpecial = any(
            special_char[i] in value for i in range(len(special_char)))

        if not isNum or not isUpper or not isLower or len(value) < 10 or not isSpecial:
            raise serializers.ValidationError(
                'Please Maintain Password Criteria')
        return value


class AadharDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AadharData
        fields = ['id', 'serial', 'card_number', 'VID', 'profile',
                  'name', 'DOB', 'gender', 'address', 'mobile']


class FIRDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIRData
        fields = ['id', 'serial', 'fir_id', 'profile', 'name',
                  'father_name', 'address', 'phone_number', 'fir_type']


class ExtractFacesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractFacesData
        fields = ['id', 'image', 'serial', 'from_database']


class CascadeAndTrainerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CascadeAndTrainerData
        fields = ['id', 'name', 'file_name']


class TrainedDataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainedDataSet
        fields = ['id', 'serial', 'name', 'aadhar_number']


class TrackingUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingUserData
        fields = ['id', 'case_id', 'username', 'user_profile', 'case_name',
                  'police_station_id', 'time_at_droped', 'date_at_droped', 'tracking_progress']


class PoliceStationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceStationData
        fields = ['station_id', 'address', 'phone', 'email']
