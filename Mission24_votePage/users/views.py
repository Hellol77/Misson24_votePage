from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, PostForm
from .models import PostResult, PersonalVote
from django.contrib.auth import login, logout, authenticate
from django.views.generic import FormView
from django.contrib import messages
import json

class LoginView(FormView):
    template_name = 'users/Django_login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=user_id, password=password)
        
        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user)

        return super().form_valid(form)

def main_view(request):
    return render(request, 'users/Django_main.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def PostUpload(request):
    if request.method == 'POST':
        if PostResult.objects.filter(user_id=request.user).exists():
            PostResult.objects.filter(user_id=request.user)[0].delete()

        team_name = request.POST['team_name']
        team_members = request.POST['team_members']
        intro_text = request.POST['intro_text']
        
        image1, image2, image3, image4 = None, None, None, None
        image_dict_values = [image1, image2, image3, image4]

        if len(request.FILES) != 0:
            image_dict_keys = list(request.FILES.keys())
            for i in range(len(request.FILES)):
                image_dict_values[i] = request.FILES[image_dict_keys[i]]

        postupload = PostResult(
            user_id = request.user,
            team_name=team_name,
            team_members=team_members,
            intro_text=intro_text,
            image1=image_dict_values[0],
            image2=image_dict_values[1],
            image3=image_dict_values[2],
            image4=image_dict_values[3],
        )
        postupload.save()
        return redirect('/main')
    else:
        if PostResult.objects.filter(user_id=request.user).exists():
            exContext = PostResult.objects.filter(user_id=request.user)[0]
            postuploadForm = PostForm(initial={"team_name":exContext.team_name, "team_members":exContext.team_members, "intro_text":exContext.intro_text})
        else:
            postuploadForm = PostForm

        context = {
            'postuploadForm': postuploadForm,
        }

        return render(request, 'users/dumi_register2.html', context)

def peerGroup_view(request):
    listall = PostResult.objects.all()
    if PersonalVote.objects.filter(user_id=request.user).exists():
        PersonalVoteDict = json.loads(PersonalVote.objects.filter(user_id=request.user)[0].dict_json)
        value = list(PersonalVoteDict.values())

    else:
        value = [0 for _ in range(len(listall))]

    for i in range(len(listall)):
        if i < len(value):
            listall[i].value = value[i]
        else:
            listall[i].value = 0

    context = {
        'listall': listall,
        'num': len(listall),
    }
    return render(request, 'users/assess.html', context)

def assessDetail_view(request, pk):
    listall = PostResult.objects.all()
    assess = get_object_or_404(PostResult, pk=pk)

    if PersonalVote.objects.filter(user_id=request.user).exists():
        PersonalVoteDict = json.loads(PersonalVote.objects.filter(user_id=request.user)[0].dict_json)
    else:
        PersonalVoteDict = {}

    id_list = []
    for i in range(len(listall)):
        id_list.append(listall[i].id)
        if listall[i].team_name not in PersonalVoteDict:
            PersonalVoteDict[listall[i].team_name] = 0
    
    if request.method == 'POST':
        if PersonalVoteDict[assess.team_name] == 1:
            PersonalVote.objects.filter(user_id=request.user)[0].delete()
            PersonalVoteDict[assess.team_name] = 0

            voteupload = PersonalVote(
                user_id = request.user,
                dict_json = json.dumps(PersonalVoteDict)
            )
            voteupload.save()
            return redirect('.')

        if sum(list(PersonalVoteDict.values())) == 5:
            messages.add_message(request, messages.INFO, 'Hello world.')
            return redirect('/assess')
        else:
            if PersonalVote.objects.filter(user_id=request.user).exists():
                PersonalVote.objects.filter(user_id=request.user)[0].delete()

            PersonalVoteDict[assess.team_name] = 1

            voteupload = PersonalVote(
                user_id = request.user,
                dict_json = json.dumps(PersonalVoteDict)
            )
            voteupload.save()

            return redirect('.')

    else:
        if id_list.index(assess.id) == 0:
            if len(listall) == 1:
                prevID = None
                nextID = None
            else:
                prevID = None
                nextID = id_list[1]
        elif id_list.index(assess.id) == len(listall)-1:
            prevID = id_list[len(listall)-2]
            nextID = None
        else:
            prevID = id_list[id_list.index(assess.id)-1]
            nextID = id_list[id_list.index(assess.id)+1]


        context = {
            'assess': assess,
            'userVoteDict': PersonalVoteDict,
            'value': PersonalVoteDict[assess.team_name],
            'num': len(listall),
            'prevID':prevID,
            'nextID':nextID,
        }

        return render(request, 'users/assess_detail.html', context)
 
