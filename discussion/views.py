from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Question, Comment, Answer, UpVoteQues, DownVoteQues, AddStar, UpVoteAns, DownVoteAns
from django.urls import reverse
from .forms import RegisterForm, LoginForm, AskQues, CommentForm, AnswerForm, UpdateForm, ChangePass
from django.core.paginator import Paginator
from django.http import JsonResponse
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
  cloud_name = "discuss",
  api_key = "736345776388642",
  api_secret = "c5Bv3wTCcytoKyNJob-K4JTFqFk"
)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_pass = form.cleaned_data['confirm_pass']
            if User.objects.filter(username=username).exists():
                error_msg = "Username already taken!"
                return render(request, 'discuss/register.html', {'error_msg':error_msg, 'form':form})
            elif User.objects.filter(email=email).exists():
                error_msg = "You are already registered!"
                return render(request, 'discuss/register.html', {'error_msg':error_msg, 'form':form})
            else:
                if password == confirm_pass:
                    newUser = User.objects.create(username=username, email=email, password=password)
                    success_msg = 'Successfully registered!'
                    return render(request, 'discuss/login.html', {'success_msg':success_msg, 'form':form})
                else:
                    error_msg = "Passwords do not match!"
                    return render(request, 'discuss/register.html', {'error_msg': error_msg, 'form': form})
        else:
            error_msg = "Error!! Try again!"
            return render(request, 'discuss/register.html', {'error_msg': error_msg, 'form':form})
    else:
        form = RegisterForm()
        return render(request, 'discuss/register.html', {'form':form})

def login(request):
    if 'is_logged_in' not in request.session or request.session['is_logged_in'] == False:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                remember_me = form.cleaned_data['remember_me']
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    user_pass = user.password
                    if user_pass == password:
                        request.session['is_logged_in'] = True
                        request.session['username'] = username
                        if remember_me == 'off':
                            request.session.set_expiry(864000)
                        else:
                            request.session.set_expiry(1300000)
                        return HttpResponseRedirect(reverse('discuss:recent'))
                    else:
                        error_msg = "Wrong Password!"
                        return render(request, 'discuss/login.html', {'form': form, 'error_msg':error_msg})
                else:
                    error_msg = "Username does not exists!"
                    return render(request, 'discuss/login.html', {'form': form, 'error_msg': error_msg})
            else:
                form = LoginForm()
                error_msg = "Error!"
                return render(request, 'discuss/login.html', {'form': form, 'error_msg': error_msg})
        else:
            form = LoginForm()
            return render(request, 'discuss/login.html', {'form': form})
    else:
        if request.session['is_logged_in']==True:
            return HttpResponseRedirect(reverse('discuss:recent'))
        else:
            form = LoginForm()
            return render(request, 'discuss/login.html', {'form':form})

def logout(request):
    request.session['is_logged_in'] = False
    return HttpResponseRedirect(reverse('discuss:login'))

def myAccount(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    form = UpdateForm()
    if 'is_logged_in' not in request.session or request.session['is_logged_in'] == False:
        return HttpResponseRedirect(reverse('discuss:login'))
    else:
        logged_user = user.username
        if user.image is not None:
            image_url = cloudinary.CloudinaryImage(user.image).build_url(width=200, height=200, crop='thumb',
                                                                         gravity='face')
        else:
            image_url = None
        return render(request, 'discuss/myaccount.html',{'user': user, 'image_url': image_url, 'logged_user': logged_user, 'form':form})


def update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    logged_user = user.username
    form = UpdateForm()
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            user.name = form.cleaned_data['name']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.bio = form.cleaned_data['bio']
            user.save()
            return render(request, 'discuss/myaccount.html', {'user': user, 'logged_user': logged_user, 'form':form})
        else:
            form = UpdateForm()
            return render(request, 'discuss/myaccount.html',{'user': user, 'logged_user': logged_user, 'form':form})
    return render(request, 'discuss/myaccount.html', {'user': user, 'logged_user': logged_user, 'form':form})


def change_pass(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = ChangePass(request.POST)
        if form.is_valid():
            current = form.cleaned_data['current']
            new = form.cleaned_data['new']
            confirm_new = form.cleaned_data['confirm_new']
            if user.password == current:
                if new == confirm_new:
                    user.password = new
                    user.save()
                    success_msg = "Password successfully changed!"
                    return render(request, 'discuss/myaccount.html', {'user': user, 'logged_user': user.username, 'form': form, 'success_msg': success_msg})
                else:
                    error_msg = "Your passwords didn't match!!"
                    return render(request, 'discuss/myaccount.html', {'user': user, 'logged_user': user.username, 'form': form, 'error_msg': error_msg })
            else:
                error_msg = "Wrong password!!"
                return render(request, 'discuss/myaccount.html', {'user': user, 'logged_user': user.username, 'form': form, 'error_msg':error_msg})
        else:
            error_msg = "Form Invalid"
            return render(request, 'discuss/myaccount.html', {'user': user, 'logged_user': user.username, 'form': form, 'error_msg': error_msg })
    else:
        form = ChangePass()
        return render(request, 'discuss/myaccount.html',{'user': user, 'logged_user': user.username, 'form': form})


def set_image(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    image = request.FILES['image']
    if user.image is not None:
        cloudinary.uploader.destroy(user.image)
    image_obj = cloudinary.uploader.upload(image, eager={'width': 200, 'height': 200, 'crop': 'thumb', 'gravity': 'face'})
    user.image = image_obj['public_id']
    user.save()
    return HttpResponseRedirect(reverse('discuss:my_account', args=(user_id,)))

def index(request):
    return HttpResponseRedirect(reverse('discuss:recent'))

def recent(request):
    if 'is_logged_in' not in request.session or request.session['is_logged_in'] == False:
        return HttpResponseRedirect(reverse('discuss:login'))
    else:
        user = get_object_or_404(User, username=request.session['username'])
        query = Question.objects.all().order_by('-pub_date')
        answers = Answer.objects.all().order_by('-pub_date')
        starred_ques = AddStar.objects.filter(user=user).values_list('question', flat=True)
        users = User.objects.all()
        logged_user = request.session['username']
        page = request.GET.get('page', 1)
        paginator = Paginator(query, 7)
        allQues = Question.objects.all()
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        context ={
            'queryset': queryset,
            'set_active': 'recent',
            'answers': answers,
            'users': users,
            'logged_user': logged_user,
            'allQues': allQues,
            'starred_ques': starred_ques,
            'user_id': user.pk,
            'user': user,
        }
        return render(request, 'discuss/recent.html', context)

def answered(request):
    user = get_object_or_404(User, username=request.session['username'])
    answers = Answer.objects.all().order_by('-pub_date')
    users = User.objects.all()
    query = Question.objects.exclude(answers=0)
    starred_ques = AddStar.objects.filter(user=user).values_list('question', flat=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(query, 7)
    allQues = Question.objects.all()
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': queryset,
        'set_active':'answered',
        'allQues':allQues,
        'answers':answers,
        'users':users,
        'starred_ques':starred_ques,
    }
    return render(request, 'discuss/recent.html', context)

def unanswered(request):
    user = get_object_or_404(User, username=request.session['username'])
    answers = Answer.objects.all().order_by('-pub_date')
    users = User.objects.all()
    query = Question.objects.filter(answers=0)
    starred_ques = AddStar.objects.filter(user=user).values_list('question', flat=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(query, 7)
    allQues = Question.objects.all()
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    return render(request, 'discuss/recent.html', {'queryset': queryset, 'set_active':'unanswered', 'allQues':allQues, 'answers':answers, 'users':users, 'starred_ques':starred_ques,})

def ask(request):
    user = get_object_or_404(User, username=request.session['username'])
    if 'is_logged_in' not in request.session or request.session['is_logged_in'] == False:
        error_msg = "Login First!!"
        return render(request, 'discuss/login.html', {'error_msg': error_msg})
    else:
        if request.method == 'POST':
            form = AskQues(request.POST)
            if form.is_valid():
                description = form.cleaned_data['description']
				title = form.cleaned_data['title']
                newQues = Question.objects.create(user=user, title=title, description=description)
                #newQues.save()
                return HttpResponseRedirect(reverse('discuss:recent'))
            else:
                return render(request, 'discuss/ask.html', {'form':form})
        else:
            form = AskQues()
            return render(request, 'discuss/ask.html', {'form':form})

def answer(request, ques):
    question = get_object_or_404(Question, pk=ques)
    user = get_object_or_404(User, username=request.session['username'])
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer_text']
            newAns = Answer.objects.create(question=question, user=user, answer_text=answer)
            question.answers += 1
            question.save()
            return HttpResponseRedirect(reverse('discuss:details', args=(ques,)))
        else:
            error_msg = "Fill form completely!"
            return HttpResponseRedirect(reverse('discuss:details', args=(ques,)))
    else:
        form = AnswerForm()
        return HttpResponseRedirect(reverse('discuss:details', args=(ques,)))

def accept(request):
    return HttpResponse('Recent')

def vote(request, ques):
    question = Question.objects.get(pk=ques)
    return HttpResponse('Recent')

def quesVotes(request):
    if request.method == "GET":
        ques = request.GET['ques']
        question = get_object_or_404(Question, pk=ques)
        votes = question.total
        return render(request, 'quesVotes.html', {'votes':votes})

def VoteUpQues(request):
    if request.method == "GET":
        ques = request.GET['ques']
        question = get_object_or_404(Question, pk=ques)
        user = get_object_or_404(User, username=request.session['username'])
        if DownVoteQues.objects.filter(user=user, question=question).exists():
            obj = DownVoteQues.objects.filter(user=user, question=question)
            obj.delete()
            question.downvotes -= 1
            question.save()
        if UpVoteQues.objects.filter(user=user, question=question).exists():
            obj = UpVoteQues.objects.get(user=user, question=question)
            obj.delete()
            question.upvotes -= 1
            question.save()
            question.total = question.upvotes - question.downvotes
            question.save()
            return JsonResponse({'total': question.total})
        else:
            obj = UpVoteQues.objects.create(question=question, user=user)
            question.upvotes += 1
            question.save()
            question.total = question.upvotes - question.downvotes
            question.save()
            return JsonResponse({ 'total':question.total })

def VoteUpAns(request):
    if request.method == "GET":
        ans = request.GET['ans']
        ques = request.GET['ques']
        answer = get_object_or_404(Answer, pk=ans)
        user = get_object_or_404(User, username=request.session['username'])
        question = get_object_or_404(Question, pk=ques)
        if DownVoteAns.objects.filter(user=user, answer=answer).exists():
            obj = DownVoteAns.objects.filter(user=user, answer=answer)
            obj.delete()
            answer.downvotes -= 1
            answer.save()
        if UpVoteAns.objects.filter(user=user, answer=answer).exists():
            obj = UpVoteAns.objects.get(user=user, answer=answer)
            obj.delete()
            answer.upvotes -= 1
            answer.save()
            answer.total = answer.upvotes - answer.downvotes
            answer.save()
            return JsonResponse({'total': answer.total})
        else:
            obj = UpVoteAns.objects.create(answer=answer, user=user, question=question)
            answer.upvotes += 1
            answer.save()
            answer.total = answer.upvotes - answer.downvotes
            answer.save()
            return JsonResponse({'total': answer.total})

def VoteDownQues(request):
    if request.method == "GET":
        ques = request.GET['ques']
        question = get_object_or_404(Question, pk=ques)
        user = get_object_or_404(User, username=request.session['username'])
        if UpVoteQues.objects.filter(user=user, question=question).exists():
            obj = UpVoteQues.objects.get(user=user, question=question)
            obj.delete()
            question.upvotes -= 1
            question.save()

        if DownVoteQues.objects.filter(user=user, question=question).exists():
            obj = DownVoteQues.objects.get(user=user, question=question)
            obj.delete()
            question.downvotes -= 1
            question.save()
            question.total = question.upvotes - question.downvotes
            question.save()
            return JsonResponse({'total': question.total})
        else:
            ob = DownVoteQues.objects.create(user=user, question=question)
            question.downvotes += 1
            question.save()
            question.total = question.upvotes - question.downvotes
            question.save()
            return JsonResponse({'total': question.total})


def VoteDownAns(request):
    if request.method == "GET":
        ans = request.GET['ans']
        ques = request.GET['ques']
        answer = get_object_or_404(Answer, pk=ans)
        user = get_object_or_404(User, username=request.session['username'])
        question = get_object_or_404(Question, pk=ques)
        if UpVoteAns.objects.filter(user=user, answer=answer).exists():
            obj = UpVoteAns.objects.filter(user=user, answer=answer)
            obj.delete()
            answer.upvotes -= 1
            answer.save()

        if DownVoteAns.objects.filter(user=user, answer=answer).exists():
            obj = DownVoteAns.objects.get(user=user, answer=answer)
            obj.delete()
            answer.downvotes -= 1
            answer.save()
            answer.total = answer.upvotes - answer.downvotes
            answer.save()
            return JsonResponse({'total': answer.total})
        else:
            ob = DownVoteAns.objects.create(user=user, answer=answer, question=question)
            answer.downvotes += 1
            answer.save()
            answer.total = answer.upvotes - answer.downvotes
            answer.save()
            return JsonResponse({'total': answer.total})

def addStar(request):
    if request.method == "GET":
        ques = request.GET['ques']
        question = Question.objects.get(pk=ques)
        user = User.objects.get(username=request.session['username'])
        if AddStar.objects.filter(user=user, question=question).exists():
            obj = AddStar.objects.filter(user=user, question=question)
            obj.delete()
            question.stars -= 1
            question.save()
        else:
            obj = AddStar.objects.create(user=user, question=question)
            question.stars += 1
            question.save()
        return JsonResponse({ 'stars':question.stars })

def details(request, ques):
    question = Question.objects.get(pk=ques)
    if User.objects.filter(username=request.session['username']).exists():
        user = User.objects.get(username=request.session['username'])
	username = request.session['username']
    else:
        user = None
    if UpVoteQues.objects.filter(question=question, user=user).exists():
        is_upvoted = True
    else:
        is_upvoted = False
    if DownVoteQues.objects.filter(question=question, user=user).exists():
        is_downvoted = True
    else:
        is_downvoted = False
    if AddStar.objects.filter(question=question, user=user).exists():
        is_starred = True
    else:
        is_starred = False
    allComments = Comment.objects.filter(question=question)
    allAnswers = Answer.objects.filter(question=question)
    upvotedAns = UpVoteAns.objects.filter(question = question).filter(user=user).values_list('answer', flat=True)
    downvotedAns = DownVoteAns.objects.filter(question = question).filter(user=user).values_list('answer', flat=True)
    answer_form = AnswerForm()

    context = {
        'ques': question,
        'allComments': allComments,
        'allAnswers':allAnswers,
        'is_upvoted':is_upvoted,
        'is_downvoted':is_downvoted,
        'is_starred':is_starred,
        'logged_user':request.session['username'],
        'downvotedAns':downvotedAns,
        'upvotedAns':upvotedAns,
        'answer_form':answer_form,
	'username': username, 
    }
    return render(request, 'discuss/details.html', context)

def comment(request, ques):
    question = Question.objects.get(pk=ques)
    user = User.objects.get(username=request.session['username'])
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            newComment = Comment.objects.create(comment=comment)
            newComment.question = question
            newComment.user = user
            newComment.save()
            allComments = Comment.objects.filter(question=question, user=user)
            allAnswers = Answer.objects.filter(question=question, user=user)
            return HttpResponseRedirect(reverse('discuss:details', args=ques))
        else:
            error_msg="error!"
            return HttpResponseRedirect(reverse('discuss:details', args=(ques,)))
    else:
        form = CommentForm()
        return HttpResponseRedirect(reverse('discuss:details', args=(ques,)))

def checkAns(request, ans, ques):
    #if request.method == "GET":
        #ans = request.GET['ans']
        #ques = request.GET['ques']
        answers = Answer.objects.get(pk=ans)
        question = Question.objects.get(pk=ques)
        #user = User.objects.get(username =ts.g request.session['username'])

        if question.user.username == request.session['username']:
            if question.is_answered == True:
                obj = Answer.objects.filter(question=question)
                for answ in obj:
                    if answ.answer == True:
                        answ.answer = False
                        answ.save()

            answers.answer = True
            answers.save(update_fields=['answer'])
            question.is_answered = True
            question.save()
            return HttpResponseRedirect(reverse('discuss:details', args=(ques,)))


