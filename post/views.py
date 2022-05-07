from django.http import JsonResponse
from django.shortcuts import render
from .models import Post
import joblib

def home(request):
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
