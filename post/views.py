from django.http import JsonResponse
from django.shortcuts import render
from .models import Post
import joblib
import wave
import requests
import json
import webbrowser

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

# def blob_table(request):
    
#     blob = request.FILES['file']
    
#     print(blob)
#     print("33333333333333ㄱ미ㅓㄹㅇ뮈ㅏ루비잘")
#     nchannels = 1
#     sampwidth = 1
#     framerate = 8000
#     nframes = 1
#     name = 'audio.wav'
#     audio = wave.open(name, 'wb')
#     audio.setnchannels(nchannels)
#     audio.setsampwidth(sampwidth)
#     audio.setframerate(framerate)
#     audio.setnframes(nframes)
#     blob = open("audio.wav").read() # such as `blob.read()`
#     audio.writeframes(blob.decode())
    
#     print(audio)
        
    
def blob_table(request):
    blob_key = request.GET.get('blob_url')
    print(blob_key)
    context = {'blob_url' : blob_key}
    
    urL=blob_key
    chrome_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open_new_tab(urL)
    
    
    
    # def download_file(url):
    #     # local_filename = url.split('/')[-1]
    #     # NOTE the stream=True parameter below
    #     with requests.get(url, stream=True) as r:
    #         r.raise_for_status()
    #         with open(url, 'wb') as f:
    #             for chunk in r.iter_content(chunk_size=8192): 
    #                 # If you have chunk encoded response uncomment if
    #                 # and set chunk_size parameter to None.
    #                 #if chunk: 
    #                 f.write(chunk)
    #     return url
    
    # download_file(blob_key)
    
    # json_txt = requests.get(blob_key).text
    # document = json.loads(json_txt)

    # print("ㅇㅇㅇㅇㅇㅇㅇㅇ")
    # print(document)
    return JsonResponse(context)

