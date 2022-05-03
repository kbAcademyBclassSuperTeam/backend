from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt  # django 의 보완문제인 csrf 를 skip하는 방법
# from sklearn.externals import joblib




nextId = 4
topics = [
    {'id':1, 'title':'routing', 'body':'Routing is ..'},
    {'id':2, 'title':'view', 'body':'View is ..'},
    {'id':3, 'title':'Model', 'body':'Model is ..'},
]

def HTMLTemplate(articleTag, id=None):


   return '''
   <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Speech Detection</title>
    </head>
    <body>

    <div class="words" contenteditable>
    </div>

    <script>
    window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    let recognition = new SpeechRecognition();
    recognition.interimResults = true;
    recognition.lang = 'ko-KR';

    let makeNewTextContent = function() {
        p = document.createElement('p');
        document.querySelector('.words').appendChild(p);
    };

    let p = null;

    recognition.start();
    recognition.onstart = function() {
        makeNewTextContent(); // 음성 인식 시작시마다 새로운 문단을 추가한다.
    };
    recognition.onend = function() {
        recognition.start();
    };

    recognition.onresult = function(e) {
        let texts = Array.from(e.results)
                .map(results => results[0].transcript).join("");

        texts.replace(/느낌표|강조|뿅/gi, '❗️');

        

        

        p.textContent = texts;
    };
    </script>


    <style>
        html {
        font-size: 10px;
        }

        body {
        background: #ffc600;
        font-family: 'helvetica neue';
        font-weight: 200;
        font-size: 20px;
        }

        .words {
        max-width: 500px;
        margin: 50px auto;
        background: white;
        border-radius: 5px;
        box-shadow: 10px 10px 0 rgba(0,0,0,0.1);
        padding: 1rem 2rem 1rem 5rem;
        background: -webkit-gradient(linear, 0 0, 0 100%, from(#d9eaf3), color-stop(4%, #fff)) 0 4px;
        background-size: 100% 3rem;
        position: relative;
        line-height: 3rem;
        }

        p {
        margin: 0 0 3rem;
        }

        .words:before {
        content: '';
        position: absolute; 
        width: 4px;
        top: 0;
        left: 30px;
        bottom: 0;
        border: 1px solid;
        border-color: transparent #efe4e4;
        }
        
    </style>
    <ul>
    {articleTag}
    </ul>
    </body>
    </html>
   '''

def index(request): # 첫번째 파라미터의 인자로 요청 객체를 전달.
    article = '''
    Hello
    '''
    return HttpResponse(HTMLTemplate(article))


def read(request, id):
    # 딕셔너리에서 숫자이여도 read로 넘어온 id는 문자열임.
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article, id))

@csrf_exempt
def create(request):
    global nextId
    if request.method == 'GET':
        article = '''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        # placeholder는 도움말, input 태그 안에 default 값
        # form 태그로 감싸줘야지 textarea에 적힌 내용을 서버로 전송 가능
        # 보내고 싶은 서버의 path는 action이라는 속성의 값으로 넣어주면 됨. (/create/ : 현재 페이지)
        return HttpResponse(HTMLTemplate(article))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id":nextId, "title":title, "body":body}
        topics.append(newTopic)
        url = '/read/'+str(nextId)
        nextId = nextId + 1
        return redirect(url) # 서버가 웹브라우저한테 redirect하라고 시킨다. django redirect

@csrf_exempt
def update(request,id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title":topic['title'],
                    "body":topic['body']
                }
        article = f'''
            <form action="/update/{id}/" method="post">
                <p><input type="text" name="title" placeholder="title" value={selectedTopic["title"]}></p>
                <p><textarea name="body" placeholder="body">{selectedTopic['body']}</textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        # 값을 채울 때는 input tag의 경우는 태그안의 value로 , textarea의 경우는 { }으로 태그안에 값을 써야한다.
        return HttpResponse(HTMLTemplate(article, id))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
        return redirect(f'/read/{id}')



@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        newTopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics
        return redirect('/')