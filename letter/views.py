import json, jwt
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from DearSanta.settings import SECRET_KEY, ALGORITHM
from accounts.models import User
from letter.models import Letter, Answer


@csrf_exempt
def write_letter(request):
    if 'Authorization' not in request.headers:
        return HttpResponse(status=401)
    if request.method == 'POST':
        payload = jwt.decode(request.headers['Authorization'][7:], SECRET_KEY, ALGORITHM)
        user = get_object_or_404(User, email=payload['email'])
        Letter.objects.create(
            dear='Santa',
            writer=user,
            content=json.loads(request.body)['content'],
            is_answer=0
        )
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


@csrf_exempt
def write_answer(request):
    if 'Authorization' not in request.headers:
        return HttpResponse(status=401)
    if request.method == 'POST':
        data = json.loads(request.body)
        payload = jwt.decode(request.headers['Authorization'][7:], SECRET_KEY, ALGORITHM)
        user = get_object_or_404(User, email=payload['email'])

        letter = Letter.objects.filter(Q(is_answer=0) & ~Q(writer=user)).first()
        letter.is_answer = 1
        letter.save()

        Answer.objects.create(
            content=data['content'],
            letter=letter,
            responser=user
        )
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


@csrf_exempt
def get_letter(request):
    if 'Authorization' not in request.headers:
        return HttpResponse(status=401)
    if request.method == 'GET':
        now = datetime.now()
        # if now.month is not 12 or now.day is not 25:
        #     print(str(now.month) + '/' + str(now.day))
        #     return HttpResponse(status=400)
        payload = jwt.decode(request.headers['Authorization'][7:], SECRET_KEY, ALGORITHM)
        user = get_object_or_404(User, email=payload['email'])
        letters = Letter.objects.filter(Q(is_answer=1) & Q(writer=user))
        res = [
            {
                'letter': {
                    'dear': 'Santa',
                    'content': letter.content,
                    'from': user.name
                },
                'answer': {
                    'dear': user.name,
                    'content': get_object_or_404(Answer, letter=letter).content,
                    'from': 'Santa'
                    # 'from': get_object_or_404(User, name=get_object_or_404(Answer, letter=letter).responser).name
                }
            }for letter in letters
        ]
        return HttpResponse(json.dumps(res), status=200)
    else:
        return HttpResponse(status=400)
