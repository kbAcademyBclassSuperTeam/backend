from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Post, Sound
from django.conf import settings
import joblib
import json
from binascii import a2b_base64
import base64
import pandas as pd
import tensorflow as tf
import librosa
import numpy as np
import itertools


def post(request):
    posts = Post.objects.all()
    data = {
        'posts': posts,
    }
    return render(request, 'home.html', data)

def model_predict(texts):
    transformer = joblib.load('post\model_folder\corpus_transformer.pkl')
    model = joblib.load('post\model_folder\corpus.pkl')
    ex = transformer.transform({texts})
    y_pred = model.predict(ex)

    return y_pred[0]
    
def search_table(request):
    search_key = request.GET.get('search_key') 
    context = {'search_key': str(model_predict(search_key))} 

    return JsonResponse(context)
    # return render(request,'home.html',context)

def blob_table(request):
    blob_key = request.GET.get('blob_url')
    context = {'blob_url' : blob_key}
    
    return JsonResponse(context)



def scam_model():
    model = tf.keras.models.load_model('post\model_folder\CNN_second_model2.h5')
    path = './test.wav'
    y, sr = librosa.load(path)
    
    n_fft = int(np.ceil(0.025 * sr))
    win_length = int(np.ceil(0.025 * sr))
    hop_length = int(np.ceil(0.01 * sr))

    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=40, win_length=win_length, hop_length=hop_length, n_fft=n_fft)
    
    print(S.shape)
    
    max_num = 14960
    arr_re = []
    
    arr_df = [ list(itertools.chain(*S)) ]
    arr_len = len(arr_df[0])
    avg = sum(arr_df[0]) / arr_len
    
    if arr_len > max_num:
        pred_now = 0
        idx = arr_len//max_num
        for i in range(idx):
            arr_re = []
            for j in range(i*max_num,(i+1)*max_num):
                arr_re.append(arr_df[0][j])

            padded_np = np.array(arr_re)

            b = padded_np.reshape(1, 40, 374)

            re_np = np.expand_dims(b, -1)

            pred = model.predict(re_np)
            print(pred)
            pred_now += pred

        if arr_len % max_num != 0:
            arr_re = []
            for i in range(arr_len - arr_len + idx * max_num, arr_len):
                arr_re.append(arr_df[0][i])
            for i in range(max_num- arr_len % max_num):
                    arr_re.append(avg)
            padded_np = np.array(arr_re)

            b = padded_np.reshape(1, 40, 374)

            re_np = np.expand_dims(b, -1)

            pred = model.predict(re_np)
            print(pred)
            pred_now += pred

        print(pred_now)
        if pred_now > 0.1:
            print(1)
        else:
            print(0)
    else:
        for i in range(arr_len):
            arr_re.append(arr_df[0][i])
        for i in range(max_num-arr_len):
            arr_re.append(avg)

        padded_np = np.array(arr_re)

        b = padded_np.reshape(1, 40, 374)

        re_np = np.expand_dims(b, -1)

        pred = model.predict(re_np)
        print(pred)
        if np.round(pred)[0][0] > 0.1:
            print(1)
        else:
            print(0)
        
        
    
    
    

def createSound(request):

    data = request.body
    url = json.loads(data).get('url')

    binary_data = decode_base64_url(url)
    with open(settings.MEDIA_ROOT + '/test.wav', 'wb') as f:
        f.write(binary_data)
        f.close()
    scam_model()
    
    
    
    
    return redirect('http://127.0.0.1:8000')

def decode_base64_url(url):
    assert url.startswith('data:audio/')
    assert ';base64,' in url
    schema, payload = url.split(',', 1)
    # Maybe parse the schema if you want to know the image's type
    # type = schema.split('/', 1)[-1].split(';', 1)[0]
    return base64.urlsafe_b64decode(payload)