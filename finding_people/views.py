
from datetime import datetime
import glob
from io import BufferedReader, BytesIO
import random
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

from finding_people.utils import Util
from .models import User, LoggedInData, AadharData, FIRData, ExtractFacesData, CascadeAndTrainerData, TrainedDataSet, TrackingUserData, PoliceStationData
from .serializers import UserSerializer, LoggedInDataSerializer, AadharDataSerializer, FIRDataSerializer, ExtractFacesDataSerializer, CascadeAndTrainerDataSerializer, TrainedDataSetSerializer, TrackingUserDataSerializer, PoliceStationDataSerializer
import json
from rest_framework import status
import uuid
from FaceRecognition.FaceRecognition import TrainImages, TakeImages, TrackImages
import cv2
import os
from pathlib import Path
from django.conf import settings


defaultURL = settings.DEFAULT_URL
# Create your views here.


@api_view(['GET'])
def home(request):
    if request.method == 'GET':
        return Response({
            'status': 200,
            'message': "Django Working!!"
        })


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def UserView(request):
    if request.method == 'GET':
        try:
            modelUser = User.objects.all()
            serializerUser = UserSerializer(modelUser, many=True)
            return Response(serializerUser.data)
        except:
            res = {
                'status': 'error',
                'message': 'No Data Found'
            }
            return responseMaker(res, status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        clientData = request.data
        clientData['mobile'] = int(clientData['mobile'])
        username = clientData.get('username')
        email = clientData.get('email')
        mobile = clientData.get('mobile')
        try:
            existingEmail = User.objects.get(email=email)
            res = {
                'status': 'error',
                'message': 'User With Same Email Already Exist',
            }
            return responseMaker(res, status.HTTP_409_CONFLICT)

        except:
            try:
                existingUsername = User.objects.get(username=username)
                res = {
                    'status': 'error',
                    'message': 'Same Username Already Taken',
                }
                return responseMaker(res, status.HTTP_409_CONFLICT)
            except:
                email_otp = int(random.randrange(100000, 999999))
                mobile_otp = int(random.randrange(100000, 999999))
                clientData['email_otp'] = email_otp
                clientData['mobile_otp'] = mobile_otp
                objectSerializer = UserSerializer(data=clientData)
                if objectSerializer.is_valid():
                    email_data = {
                        'type': 'otp',
                        'otp': email_otp,
                        'email_to': email,
                        'username': username
                    }
                    Util.send_email(email_data)

                    mobile_data = {
                        'otp': mobile_otp,
                        'mobile': str(mobile)
                    }

                    # Util.send_sms(mobile_data)

                    objectSerializer.save()
                    res = {
                        'status': 'success',
                        'message': 'User Created Successfully',
                    }
                    return responseMaker(res, status.HTTP_201_CREATED)
                print(objectSerializer.errors)
                return errorResponseMaker(objectSerializer.errors)

    if request.method == 'PUT':
        clientData = request.data
        username = clientData.get('username')
        try:
            Userdetails = User.objects.get(username=username.lower())
            objectSerializer = UserSerializer(
                Userdetails, data=clientData, partial=True)
            if objectSerializer.is_valid():
                objectSerializer.save()
                res = {
                    'status': 'success',
                    'message': 'Successfully Updated',
                }
                return responseMaker(res, status.HTTP_201_CREATED)

            return errorResponseMaker(objectSerializer.errors)
        except:
            res = {
                'status': 'error',
                'message': 'No User Found',
            }
            return responseMaker(res, status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        clientData = request.data
        username = clientData.get('username')
        try:
            Userdetails = User.objects.get(username=username)
            Userdetails.delete()
            res = {
                'status': 'success',
                'message': 'Successfully Deleted',
            }
            return responseMaker(res, status.HTTP_202_ACCEPTED)
        except:
            res = {
                'status': 'error',
                'message': 'No User Found',
            }
            return responseMaker(res, status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def VerifyUser(request):
    if request.method == 'POST':
        clientData = request.data
        username = clientData.get('username')
        if clientData['verification_off'] == 'email':
            try:
                Userdetails = User.objects.get(username=username)
                tableData = UserSerializer(Userdetails).data
                if clientData['email_otp'] == tableData['email_otp']:
                    clientData = {
                        'email_otp': None,
                        'email_verification': True
                    }
                    objectSerializer = UserSerializer(
                        Userdetails, data=clientData, partial=True)

                    if objectSerializer.is_valid():
                        objectSerializer.save()
                        res = {
                            'status': 'success',
                            'message': 'Email Verified Successfully',
                        }
                        return responseMaker(res, status.HTTP_201_CREATED)

                    return errorResponseMaker(objectSerializer.errors)
                else:
                    res = {
                        'status': 'error',
                        'message': 'Invalid OTP',
                    }
                    return responseMaker(res, status.HTTP_404_NOT_FOUND)
            except Exception as e:
                res = {
                    'status': 'error',
                    'message': 'No User Found',
                }
                return responseMaker(res, status.HTTP_404_NOT_FOUND)
        elif clientData['verification_off'] == 'phone':
            try:
                Userdetails = User.objects.get(username=username)

                tableData = UserSerializer(Userdetails).data
                if clientData['mobile_otp'] == tableData['mobile_otp']:

                    clientData = {
                        'mobile_otp': None,
                        'mobile_verification': True
                    }
                    objectSerializer = UserSerializer(
                        Userdetails, data=clientData, partial=True)

                    if objectSerializer.is_valid():
                        objectSerializer.save()
                        res = {
                            'status': 'success',
                            'message': 'Mobile Number Verified Successfully',
                        }
                        return responseMaker(res, status.HTTP_201_CREATED)

                    return errorResponseMaker(objectSerializer.errors)
                else:
                    res = {
                        'status': 'error',
                        'message': 'Invalid OTP',
                    }
                    return responseMaker(res, status.HTTP_404_NOT_FOUND)
            except Exception as e:
                res = {
                    'status': 'error',
                    'message': 'No User Found',
                }
                return responseMaker(res, status.HTTP_404_NOT_FOUND)


# Main functions starts
@api_view(['POST'])
def UserLogin(request):
    if request.method == 'POST':
        clientData = request.data
        return LoginTrigger(clientData, True)


@api_view(['POST'])
def UserLogout(request):
    if request.method == 'POST':
        userData = request.data
        session = userData.get('session')
        try:
            tableData = LoggedInDataSerializer(
                LoggedInData.objects.get(session=session)).data

            data = {
                'username': tableData.get('username'),
                'session': ''
            }
            loginSerializer = LoggedInDataSerializer(
                LoggedInData.objects.get(session=session), data=data, partial=True)

            if loginSerializer.is_valid():
                loginSerializer.save()
                res = {
                    'status': 'success',
                    'message': 'Successfully Logged Out',
                }
                return responseMaker(res, status.HTTP_202_ACCEPTED)
            return errorResponseMaker(loginSerializer.errors)

        except:
            res = {
                'status': 'error',
                'message': 'Wrong Session ID',
            }
            return responseMaker(res, status.HTTP_404_NOT_FOUND)

# Mine Function


def LoginTrigger(clientData, needReturn):
    if clientData.get('username') is not None:
        try:
            username = clientData.get('username')
            userData = UserSerializer(User.objects.get(username=username)).data
            if check_password(clientData['password'], userData['password']):
                session = str(uuid.uuid4())

                while(True):
                    if checkForSessionIdExist(session):
                        break
                    session = str(uuid.uuid4())

                LoggedInTableUpdate(username, session)

                if needReturn:

                    res = {
                        'status': 'success',
                        'message': 'Successfully Logged In',
                        'session_id': session
                    }
                    return responseMaker(res, status.HTTP_200_OK)
            else:
                if needReturn:
                    res = {
                        'status': 'error',
                        'message': 'Password Mismatched'
                    }
                    return responseMaker(res, status.HTTP_400_BAD_REQUEST)

        except:
            if needReturn:
                res = {
                    'status': 'error',
                    'message': 'Username Not Exist'
                }
                return responseMaker(res, status.HTTP_404_NOT_FOUND)

    else:
        try:
            email = clientData.get('email')
            userData = UserSerializer(User.objects.get(email=email)).data

            if userData['password'] == clientData.get('password'):

                session = str(uuid.uuid4())

                while(True):
                    if checkForSessionIdExist(session):
                        break
                    session = str(uuid.uuid4())

                LoggedInTableUpdate(username, session)
                if needReturn:
                    res = {
                        'status': 'success',
                        'message': 'Successfully Logged In',
                        'session_id': session
                    }
                    return responseMaker(res, status.HTTP_200_OK)
            else:
                if needReturn:
                    res = {
                        'status': 'error',
                        'message': 'Password Mismatched'
                    }
                    return responseMaker(res, status.HTTP_400_BAD_REQUEST)
        except:
            if needReturn:
                res = {
                    'status': 'error',
                    'message': 'Email Not Exist'
                }
                return responseMaker(res, status.HTTP_404_NOT_FOUND)


def LoggedInTableUpdate(username, session):
    loggedData = {
        'username': username,
        'session': session
    }

    try:
        tableData = LoggedInData.objects.get(username=username)
        loginSerializer = LoggedInDataSerializer(tableData, data=loggedData)
        if loginSerializer.is_valid():
            loginSerializer.save()
            return True
        return False

    except:
        loginSerializer = LoggedInDataSerializer(data=loggedData)
        if loginSerializer.is_valid():
            loginSerializer.save()
            return True
        return False


def checkForSessionIdExist(session):
    try:
        userData = LoggedInDataSerializer(
            LoggedInData.objects.get(session=session)).data
        return False
    except:
        return True


def responseMaker(comingRes, statusCode):
    res = {}
    key = list(comingRes)
    value = list(comingRes.values())

    for i in range(0, len(key)):
        res[key[i]] = value[i]
    return Response(res, statusCode)


def errorResponseMaker(error):
    res = {'status': 'error'}
    jsonData = json.loads(json.dumps(error))
    keys = list(jsonData.keys())
    for i in range(len(keys)):
        res[keys[i]] = jsonData[keys[i]][0]

    return Response(res, status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST', 'DELETE'])
def FaceRecognize(request):

    if request.method == 'DELETE':
        var = TrackingUserData.objects.all().delete()
        files = glob.glob(os.path.join(
            Path(__file__).parent.parent, 'staticFiles\\TrackingImage\\*'))
        for f in files:
            os.remove(f)
        res = {
            'status': 'success',
            'message': 'All Files and Database Table Been Cleared'
        }
        return responseMaker(res, status.HTTP_202_ACCEPTED)

    if request.method == 'POST':
        clientData = request.data.dict()
        session = clientData['session']
        try:
            case_id = str(datetime.now()).replace(
                "-", "").replace(" ", "").replace(":", "").replace(".", "")[2:]

            tableData = LoggedInData.objects.get(session=session)
            username = LoggedInDataSerializer(tableData).data['username']
            clientData['username'] = username
            clientData['case_id'] = case_id
            clientData.pop('session')
            serializeTracking = TrackingUserDataSerializer(data=clientData)

            if serializeTracking.is_valid():
                serializeTracking.save()
                police_email = 'champprince92@gmail.com'
                try:
                    police_email = PoliceStationDataSerializer(PoliceStationData.objects.get(
                        station_id=clientData['police_station_id'])).data['email']
                except:
                    pass
                verify_link = defaultURL+"/police/verification/"+case_id

                email_data = {
                    'type': 'police_verification',
                    'name': username,
                    'email_to': police_email,
                    'verify_link': verify_link
                }
                Util.send_email(email_data)

            else:
                return Response(serializeTracking.errors, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            res = {
                'status': 'error',
                'message': 'Session Id Not Found'
            }
            return responseMaker(res, status.HTTP_404_NOT_FOUND)

        tableData = TrackingUserDataSerializer(
            TrackingUserData.objects.filter(username=username), many=True).data
        idd = -1
        index = 0
        for i in range(len(tableData)):
            if int(tableData[i]['case_id']) > idd:
                index = i
                idd = int(tableData[i]['case_id'])
        tableData = tableData[index]
        idd = int(tableData['case_id'])

        img = defaultURL + tableData['user_profile']
        data = TrackImages(img)

        num = data[0]
        if not num == 'Unknown':
            recoveredbytes = num.to_bytes(
                (num.bit_length() + 7) // 8, 'little')
            num = recoveredbytes.decode('utf-8')

            from_db = int(num.split('-')[0])
            serial = int(num.split('-')[1])
            if from_db == 1:
                data = AadharDataSerializer(
                    AadharData.objects.get(serial=serial)).data
                return Response(data, status.HTTP_200_OK)

            elif from_db == 2:
                data = FIRDataSerializer(
                    FIRData.objects.get(serial=serial)).data
                return Response(data, status.HTTP_200_OK)

        else:
            res = {
                'status': 'error',
                'message': 'Data Not Found'
            }
            return responseMaker(res, status.HTTP_404_NOT_FOUND)


###################################################### admin urls #######################################################################
@csrf_exempt
@api_view(['GET', 'DELETE'])
def ExtractFaces(request):
    if request.method == 'DELETE':
        clearingAllTheData = ExtractFacesData.objects.all().delete()
        files = glob.glob(os.path.join(
            Path(__file__).parent.parent, 'staticFiles\\TrainingImage\\*'))

        for f in files:
            os.remove(f)
        res = {
            'status': 'success',
            'message': 'All Files and Database Table Been Cleared'
        }
        return responseMaker(res, status.HTTP_202_ACCEPTED)

    if request.method == 'GET':
        # dealing with aadhar data
        modelAadhar = AadharData.objects.all()
        serializerAadhar = AadharDataSerializer(modelAadhar, many=True).data
        serializerAadhar = [dict(_) for _ in serializerAadhar]

        res = False
        if len(serializerAadhar) > 0:
            for i in serializerAadhar:
                url = defaultURL + i['profile']
                serial = i['profile'].split('/')[-1].split('.')[0]

                faceImg = TakeImages(url)
                i = 0
                for img in faceImg:
                    convertedImg = cv2_to_normal_image(img, serial)
                    res = SaveIntoTrainigImageTable(
                        convertedImg, serial, 'aadhar')
                    if res == False:
                        break
                    i += 1

                if res == False:
                    break
        else:
            resp = {
                'status': 'error',
                'message': 'No Data in AADHAR Table',
            }
            return responseMaker(resp, status.HTTP_400_BAD_REQUEST)

        # dealing with FIR data
        modelFir = FIRData.objects.all()
        firSerializer = FIRDataSerializer(modelFir, many=True).data
        firSerializer = [dict(_) for _ in firSerializer]
        res = False
        if len(firSerializer) > 0:

            for i in firSerializer:
                url = defaultURL + i['profile']
                serial = i['profile'].split('/')[-1].split('.')[0]

                faceImg = TakeImages(url)
                i = 0
                for img in faceImg:
                    convertedImg = cv2_to_normal_image(img, serial)
                    res = SaveIntoTrainigImageTable(
                        convertedImg, serial, 'fir')
                    if res == False:
                        break
                    i += 1

                if res == False:
                    break
        else:
            resp = {
                'status': 'error',
                'message': 'No Data in FIR Table',
            }
            return responseMaker(resp, status.HTTP_400_BAD_REQUEST)

        if res == True:
            modelTrainingImage = ExtractFacesData.objects.all()
            trainingImageSerializer = ExtractFacesDataSerializer(
                modelTrainingImage, many=True).data
            urls = []
            for i in trainingImageSerializer:
                urls.append(defaultURL + i['image'])
            trainer = TrainImages(urls)
            try:
                cascadeData = CascadeAndTrainerData.objects.get(
                    name='trainner')
                requests.put('http://127.0.0.1:8000/adm/cascadeandtrainer',
                             files={'file_name': trainer}, data={'name': 'trainner'})
            except:
                requests.post('http://127.0.0.1:8000/adm/cascadeandtrainer',
                              files={'file_name': trainer}, data={'name': 'trainner'})
            res = {
                'status': 'success',
                'message': 'Trainner File Saved Successfully!'
            }
            return responseMaker(res, status.HTTP_200_OK)
        else:
            resp = {
                'status': 'error',
                'message': 'Something Want Wrong on Saving Training Images',
            }
            return responseMaker(resp, status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'POST'])
def AadharDetail(request):
    if request.method == 'GET':
        clientData = request.data
        aadhar_num = clientData.get('aadhar_number')
        try:
            serializerAadhar = AadharDataSerializer(
                AadharData.objects.get(aadhar_number=aadhar_num)).data
            return Response(serializerAadhar, status.HTTP_200_OK)
        except:
            res = {
                'status': 'error',
                'message': 'No Aadhar Detail Found!'
            }
            return responseMaker(res, status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        userAadhar = request.data
        serializerAadhar = AadharDataSerializer(data=userAadhar)
        if serializerAadhar.is_valid():
            serializerAadhar.save()
            res = {
                'status': 'success',
                'message': 'Created Successfully',
            }
            return responseMaker(res, status.HTTP_201_CREATED)

        return errorResponseMaker(serializerAadhar.errors)


def cv2_to_normal_image(img_arr, serial):
    ret, img_encode = cv2.imencode('.jpg', img_arr)
    str_encode = img_encode.tostring()
    img_byteio = BytesIO(str_encode)
    img_byteio.name = str(serial)+'.jpg'
    reader = BufferedReader(img_byteio)
    return reader


def SaveIntoTrainigImageTable(img, serial, from_db):

    res = requests.post('http://127.0.0.1:8000/adm/trainimages',
                        files={'image': img}, data={'serial': serial, 'from_database': from_db})
    status = res.json()
    if status['status'] == 'success':
        return True

    return False


@api_view(['POST'])
def TrainImageAndSave(request):
    if request.method == 'POST':
        trainingData = request.data

        serializerTrainingImage = ExtractFacesDataSerializer(data=trainingData)
        if serializerTrainingImage.is_valid():
            serializerTrainingImage.save()
            res = {
                'status': 'success'
            }
            return responseMaker(res, status.HTTP_200_OK)

        res = {
            'status': 'error'
        }
        return responseMaker(res, status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT'])
def CascadeFileAndTrainer(request):
    if request.method == 'POST':
        userData = request.data
        cascadeSerializer = CascadeAndTrainerDataSerializer(data=userData)
        if cascadeSerializer.is_valid():
            cascadeSerializer.save()
            if userData['name'] == 'cascade':
                res = {
                    'status': 'success',
                    'message': 'Successfully Inserted Cascade File'
                }
            else:
                res = {
                    'status': 'success',
                    'message': 'Successfully Inserted Trainer File'
                }
            return responseMaker(res, status.HTTP_201_CREATED)
        return errorResponseMaker(cascadeSerializer.errors)

    if request.method == 'PUT':
        userData = request.data
        name = userData['name']
        cascadeData = CascadeAndTrainerData.objects.get(name=name)

        cascadeSerializer = CascadeAndTrainerDataSerializer(
            cascadeData, data=userData)
        cascadeData.delete()
        if cascadeSerializer.is_valid():
            cascadeSerializer.save()
            if name == 'cascade':
                res = {
                    'status': 'success',
                    'message': 'Successfully Updated Cascade File'
                }
            else:
                res = {
                    'status': 'success',
                    'message': 'Successfully Updated Trainer File'
                }
            return responseMaker(res, status.HTTP_201_CREATED)
        return errorResponseMaker(cascadeSerializer.errors)


@api_view(['GET', 'POST'])
def FIRDataSaver(request):
    if request.method == 'GET':
        tableData = FIRDataSerializer(FIRData.objects.all(), many=True).data
        return Response(tableData, status.HTTP_200_OK)

    if request.method == 'POST':
        userData = request.data
        firSerializer = FIRDataSerializer(data=userData)
        if firSerializer.is_valid():
            firSerializer.save()
            res = {
                'status': 'success',
                'message': 'Data Successfully Inserted'
            }
            return responseMaker(res, status.HTTP_201_CREATED)
        return errorResponseMaker(firSerializer.errors)


@api_view(['GET', 'POST', 'DELETE'])
def PoliceStationDataFunction(request):
    if request.method == 'GET':
        tableData = PoliceStationDataSerializer(
            PoliceStationData.objects.all(), many=True).data
        return Response(tableData, status.HTTP_200_OK)

    if request.method == 'POST':
        userData = request.data
        StationSerializer = PoliceStationDataSerializer(data=userData)
        if StationSerializer.is_valid():
            StationSerializer.save()
            res = {
                'status': 'success',
                'message': 'Data Successfully Inserted'
            }
            return responseMaker(res, status.HTTP_201_CREATED)
        return errorResponseMaker(StationSerializer.errors)

    if request.method == 'DELETE':
        var = PoliceStationData.objects.all().delete()
        res = {
            'status': 'success',
            'message': 'All Database Data Been Cleared'
        }
        return responseMaker(res, status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def SuspectArrivePoliceStation(request, case_id):
    if request.method == 'GET':
        already_verified = TrackingUserDataSerializer(
            TrackingUserData.objects.get(case_id=case_id)).data['tracking_progress']
        if not already_verified == 'at Police Station':
            data = {
                'tracking_progress': 'at Police Station'
            }

            trackingSerializer = TrackingUserDataSerializer(
                TrackingUserData.objects.get(case_id=case_id), data=data, partial=True)

            if trackingSerializer.is_valid():
                trackingSerializer.save()
                return render(request, 'ThankYou/thankYou.html')
        return render(request, 'notfound/notFound.html')


@api_view(['POST'])
def ValidateUsername(request):
    if request.method == "POST":
        userData = request.data
        serializerUser = UserSerializer(User.objects.all(), many=True).data
        returnValue = True
        for data in serializerUser:
            if data['username'].lower() == userData['username'].lower():
                returnValue = False
        if returnValue:
            res = {
                'status': 'success',
                'message': 'Valid Username'
            }
            return responseMaker(res, status.HTTP_202_ACCEPTED)
        else:
            res = {
                'status': 'error',
                'message': 'Not a Valid Username'
            }
            return responseMaker(res, status.HTTP_409_CONFLICT)


@api_view(['POST'])
def ValidateMobile(request):
    if request.method == "POST":
        userData = request.data
        userData['mobile'] = int(userData['mobile'])
        serializerUser = UserSerializer(User.objects.all(), many=True).data
        returnValue = True
        for data in serializerUser:
            if data['mobile'] == userData['mobile']:
                returnValue = False
        if returnValue:
            res = {
                'status': 'success',
                'message': 'Valid Mobile'
            }
            return responseMaker(res, status.HTTP_202_ACCEPTED)
        else:
            res = {
                'status': 'error',
                'message': 'Not a Valid Mobile'
            }
            return responseMaker(res, status.HTTP_409_CONFLICT)


@api_view(['POST'])
def ValidateEmail(request):
    if request.method == "POST":
        userData = request.data
        serializerUser = UserSerializer(User.objects.all(), many=True).data
        returnValue = True
        for data in serializerUser:
            if data['email'].lower() == userData['email'].lower():
                returnValue = False
        if returnValue:
            res = {
                'status': 'success',
                'message': 'Valid Email'
            }
            return responseMaker(res, status.HTTP_202_ACCEPTED)
        else:
            res = {
                'status': 'error',
                'message': 'Not a Valid Email'
            }
            return responseMaker(res, status.HTTP_409_CONFLICT)
