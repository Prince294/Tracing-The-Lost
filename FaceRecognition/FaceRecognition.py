import cv2
from pathlib import Path
import os
import requests
import numpy as np
from PIL import Image
import datetime
import time
from io import BytesIO


######################################################################################################################

def getImagesAndLabels(urls):
    faces = []
    Ids = []
    for url in urls:
        name = url.split('/')[-1]
        response = requests.get(url)
        response = BytesIO(response.content)
        pilImage = Image.open(response).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        
        mystring = name.split('.')[0].split('-')[0]+"-"+name.split('.')[0].split('-')[1]
        mybytes = mystring.encode('utf-8')
        ID = int.from_bytes(mybytes, 'little')
        
        faces.append(imageNp)
        Ids.append(ID)
    return faces,Ids


#######################################################################################################################

def TrainImages(urls):
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    faces, ID = getImagesAndLabels(urls)
    try:
        recognizer.train(faces,np.array(ID))
    except Exception as e:
        print(e)
        return
    recognizer.save(os.path.join(Path(__file__).parent, "TrainingImageLabel/trainner.yml"))
    
    train = open(os.path.join(Path(__file__).parent, "TrainingImageLabel/trainner.yml"),'rb')
    return train


########################################################################################################################

def TakeImages(img):
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(os.path.join(Path(__file__).parent,harcascadePath))
    # reading image using URL and then conversion it to cv2 readable
    name = img.split('/')[-1]
    # urllib.request.urlretrieve(img,name)
    
    response = requests.get(img)
    img = Image.open(BytesIO(response.content))
    
    # img = Image.open(name)
    cv2_img = np.array(img)
    img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
    
    imageNeedToCapture = 5
    facesArr = []
    while True:
        imageNeedToCapture-=1
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.05, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
            image = gray[y:y + h, x:x + w]
            imgResize = cv2.resize(image, (220, 220), interpolation=cv2.INTER_AREA)

            adjusted = cv2.addWeighted(imgResize, 0.85, imgResize, 0, 1)
            
            cv2.destroyAllWindows()
            facesArr.append(adjusted)
        if imageNeedToCapture==0:
            break
    
    return facesArr



########################################################################################################################

def TrackImages(img):
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(os.path.join(Path(__file__).parent,harcascadePath))
    
    name = img.split('/')[-1]
    response = requests.get(img)
    img = Image.open(BytesIO(response.content))
    cv2_img = np.array(img)
    img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    file = r"CascadeAndTrainer\trainner.yml"
    recognizer.read(os.path.join(Path(__file__).parent.parent,file))

    date = ""
    timeStamp = ""
    
    retest=5
    
    while True:
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.05, 5)
        for (x, y, w, h) in faces:
        
            cv2.rectangle(img, (x, y), (x + w, y + h), (225, 255, 0), 2)
            image = gray[y:y + h, x:x + w]
            imgResize = cv2.resize(image, (220, 220))

            adjusted = cv2.addWeighted(imgResize, 0.85, imgResize, 0, 1)
            
        
            serial, conf = recognizer.predict(adjusted)
            print("Confidence Level is: ",conf)
            if (conf < 70):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                retest=0
            else:
                serial = "Unknown"
                
        if retest == 0:
            break
        retest-=1
            
    lis = [serial,date,timeStamp]
    return lis
        

######################################################## testing ################################################################
