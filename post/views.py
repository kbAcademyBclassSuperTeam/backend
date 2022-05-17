from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Post, Sound
from django.conf import settings
import joblib
import json
from binascii import a2b_base64
import base64


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

def createSound(request):

    data = request.body
    url = json.loads(data).get('url')

    binary_data = decode_base64_url(url)
    with open(settings.MEDIA_ROOT + '/test.wav', 'wb') as f:
        f.write(binary_data)
        f.close()
    
    return redirect('http://127.0.0.1:8000')

def decode_base64_url(url):
    assert url.startswith('data:audio/')
    assert ';base64,' in url
    schema, payload = url.split(',', 1)
    # Maybe parse the schema if you want to know the image's type
    # type = schema.split('/', 1)[-1].split(';', 1)[0]
    return base64.urlsafe_b64decode(payload)