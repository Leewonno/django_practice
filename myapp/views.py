from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt


next_id = 3
topics = [
    {'id':1, 'title':'rounting', 'body':'Rounting is...'},
    {'id':2, 'title':'view', 'body':'View is...'},
    {'id':3, 'title':'model', 'body':'Model is...'},
]

def HTMLTemplate(article, id=None):
    global topics
    contextUI = ''
    
    if id != None:
        contextUI = f'''
            <li>
                <form action="/delete/" method="post">
                    <input type hidden name="id" value={id}>
                    <input type="submit" value="Delete">
                </form>
            </li>
            <li>
                <a href="/update/{id}">Update</a>
            </li>
        '''
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ol>
                {ol}
            </ol>
            {article}
            <ul>
                <li><a href="/create">Create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''

# Create your views here.
def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, Django
    '''
    
    return HttpResponse(HTMLTemplate(article))

@csrf_exempt
def create(request):
    if request.method == "GET":
        article = '''
        <form action="/create/" method="post">
            <input type="text" name="title" placeholder="title">
            <br />
            <br />
            <textarea placeholder="body" name="body"></textarea>
            <br />
            <br />
            <input type="submit">
        </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == "POST":
        global next_id
        # print(request.POST['title'])
        # print(request.POST)
        title = request.POST['title']
        body = request.POST['body']
        next_id = next_id + 1
        url = '/read/' + str(next_id)
        newTopic = {'id':next_id, 'title':title, 'body':body}
        topics.append(newTopic)
        return redirect(url)

def read(req, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article, id))

@csrf_exempt
def delete(req):
    global topics
    if req.method == "POST":
        id = req.POST['id']
        newTopics = []
        for topic in topics:
            if(topic['id'] != int(id)):
                newTopics.append(topic)
        topics = newTopics
        return redirect('/')
    
@csrf_exempt
def update(req, id):
    global topics
    if req.method == "GET":
        title = ''
        body = ''
        for topic in topics:
            if topic['id'] == int(id):
                title = topic['title']
                body = topic['body']
        article = f'''
            <form action="/update/{id}/" method="post">
                <input type="text" name="title" value={title} placeholder="title">
                <br />
                <br />
                <textarea placeholder="body" name="body">{body}</textarea>
                <br />
                <br />
                <input type="submit" value="수정">
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif req.method == "POST":
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = req.POST['title']
                topic['body'] = req.POST['body']
        return redirect('/')