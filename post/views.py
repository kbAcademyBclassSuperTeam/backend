from django.http import JsonResponse
from django.shortcuts import render
from .models import Post
# import text_classfication
import joblib
import os



# Create your views here.
def home(request):

    posts = Post.objects.all()
    
    data = {
        'posts': posts,
    }

    return render(request, 'home.html', data)


def model_predict(texts):

    # currentPath = os.getcwd()
    # print(currentPath)
    # transformer_path = os.chdir(currentPath + "\\corpus_transformer.pkl")
    # model_path = os.chdir(currentPath + "\\corpus.pkl")

    # ------------
        
    # transformer = joblib.load('corpus_transformer.pkl') 

    # model = joblib.load('corpus.pkl')


    # ex = transformer.transform({texts})
    # y_pred = model.predict(ex)

    # return y_pred[0]
    
    return '하이'
    

def search_table(request):
    search_key = request.GET.get('search_key') 

    

    context = {'search_key': model_predict(search_key)} 

    return JsonResponse(context)
    # return render(request,'home.html',context)
