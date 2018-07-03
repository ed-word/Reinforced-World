from django.shortcuts import render
from django.http import JsonResponse
import os
from django.conf import settings
import subprocess
from .modules import fire_detection

# Create your views here.

BASE_PATH = os.getcwd()
CLASSIFICATION_PATH = os.path.join(BASE_PATH, 'angelapp', 'modules', 'classification')

DEBUG_ML = False

def index(req):
    return render(req, 'index.html', {})

def video_home(req):
    return render(req, 'video.html', {})

def check_crash_video(req):
    if DEBUG_ML:
        return JsonResponse({'result': True, 'video_url': '/media/videos/fire2.mp4', 'crash': True, 'certainty': 80.99999})

    print(req.FILES)
    f = req.FILES['myFile']
    print(f)
    with open(os.path.join(settings.MEDIA_ROOT, 'videos', f.name), 'wb+') as ff:
        for chunk in f.chunks():
            ff.write(chunk)

    ext = os.path.splitext(f.name)[1]

    with open(os.path.join(CLASSIFICATION_PATH, 'Data', 'video' + ext), 'wb') as ff:
        for chunk in f.chunks():
            ff.write(chunk)
    
    subprocess.call([os.path.join(CLASSIFICATION_PATH, 'predict.sh')])

    a = []
    with open(os.path.join(CLASSIFICATION_PATH, 'Data', 'result.txt'), 'r') as ff:
        for line in ff:
            a.append(float(line.strip()))

    posN = a[0]
    negN = a[1]
    ans = posN >= negN

    return JsonResponse({'result': True, 'video_url': '/media/videos/' + f.name, 'crash': ans, 'certainty': max(posN, negN)})

def check_fire(req):
    ret = fire_detection.detect()
    print(ret[1])
    return JsonResponse({'result': True, 'fire': ret[1], 'video_url': 'media/output.avi'})

def check_damage(req):
    return JsonResponse({'result': True})

def image_home(req):
    return render(req, 'image.html', {})

def check_image_crash(req):
    img = req.FILES['myFile']
    with open(os.path.join(settings.MEDIA_ROOT, 'image-train', f.name), 'wb+') as f:
        for chunk in img.chunks():
            f.write(chunk)

    url = '/media/image-train/{}'.format(f.name)
    return JsonResponse({'result': True, })
