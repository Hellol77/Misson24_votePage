from xml.etree.ElementTree import tostring
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, PostForm
from .models import PostResult, PersonalVote
from django.contrib.auth import login, logout, authenticate
from django.views.generic import FormView
from django.contrib import messages
import json, os
from users.decorators import *
import boto3
from botocore.client import Config
from boto.s3.connection import S3Connection

AWS_STORAGE_BUCKET_NAME = 'mission24'

s3 = boto3.resource(
        's3',
        aws_access_key_id='AKIAUXAABXZFUQ26FGPV',
        aws_secret_access_key='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',
        config=Config(signature_version='s3v4')
    )


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

@login_message_required
def main_view(request):
    return render(request, 'users/Django_main.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@login_message_required
def PostUpload(request):
    if request.method == 'POST':
        team_name = request.POST['team_name']
        team_members = request.POST['team_members']
        intro_text = request.POST['intro_text']
        
        image1, image2, image3, image4 = None, None, None, None
        image_dict_values = [image1, image2, image3, image4]

        if len(request.FILES) != 0:
            image_dict_keys = list(request.FILES.keys())
            for i in range(len(request.FILES)):
                image_dict_values[i] = request.FILES[image_dict_keys[i]]
            
            print(image_dict_values)

        if PostResult.objects.filter(user_id=request.user).exists():
            modifyPost = PostResult.objects.get(id=get_object_or_404(PostResult, user_id=request.user).id)
            modifyPost.user_id = request.user
            modifyPost.team_name = team_name
            modifyPost.team_members = team_members
            modifyPost.intro_text = intro_text

            imagesrc1, imagesrc2, imagesrc3, imagesrc4 = None, None, None, None
            src_dict_values = [imagesrc1, imagesrc2, imagesrc3, imagesrc4]

            for i in range(4):
                if image_dict_values[i] != None:
                    s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(
                    Key=team_name+"_"+str(i+1), Body=image_dict_values[i], ContentType='image/jpg')
                    src_dict_values[i] = team_name+"_"+str(i+1)
            '''
            modifyPost.image1 = image_dict_values[0]
            modifyPost.image2 = image_dict_values[1]
            modifyPost.image3 = image_dict_values[2]
            modifyPost.image4 = image_dict_values[3]
            modifyPost.save()
            '''
            modifyPost.imagesrc1 = src_dict_values[0]
            modifyPost.imagesrc2 = src_dict_values[1]
            modifyPost.imagesrc3 = src_dict_values[2]
            modifyPost.imagesrc4 = src_dict_values[3]
            modifyPost.save()
            return redirect('/main')






        else:
            postupload = PostResult(
                user_id = request.user,
                team_name=team_name,
                team_members=team_members,
                intro_text=intro_text,



                imagesrc1=image_dict_values[0],
                imagesrc2=image_dict_values[1],
                imagesrc3=image_dict_values[2],
                imagesrc4=image_dict_values[3],
            )
            postupload.save()
            return redirect('/main')
    else:
        if PostResult.objects.filter(user_id=request.user).exists():
            exContext = PostResult.objects.filter(user_id=request.user)[0]
#            postuploadForm = PostForm(initial={"team_name":exContext.team_name, "team_members":exContext.team_members, "intro_text":exContext.intro_text})

            context = {
                "team_name":exContext.team_name,
                "team_members":exContext.team_members,
                "intro_text":exContext.intro_text,
                "num": 1
            #'postuploadForm': postuploadForm,
            }
        else:
            context = {
                "num": 0
            }


        return render(request, 'users/register.html', context)

@login_message_required
def peerGroup_view(request):
    listall = PostResult.objects.all()
    if PersonalVote.objects.filter(user_id=request.user).exists():
        PersonalVoteDict = json.loads(PersonalVote.objects.filter(user_id=request.user)[0].dict_json)

        for i in range(len(listall)):
            id = listall[i].id
            if str(id) in PersonalVoteDict:
                listall[i].value = PersonalVoteDict[str(id)]
            else:
                listall[i].value = 0
    else:
        for i in range(len(listall)):
            listall[i].value = 0

    context = {
        'listall': listall,
        'num': len(listall),
    }
    return render(request, 'users/assess.html', context)

@login_message_required
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
        if str(listall[i].id) not in PersonalVoteDict:
            PersonalVoteDict[str(listall[i].id)] = 0
    
    if request.method == 'POST':

        for i in list(PersonalVoteDict.keys()):
            if int(i) not in id_list:
                del PersonalVoteDict[i]

        if PersonalVoteDict[str(assess.id)] == 1:
#            PersonalVote.objects.filter(user_id=request.user)[0].delete()
            modifyVote = PersonalVote.objects.get(id=get_object_or_404(PersonalVote, user_id=request.user).id)
            PersonalVoteDict[str(assess.id)] = 0
            modifyVote.user_id = request.user
            modifyVote.dict_json = json.dumps(PersonalVoteDict)
            modifyVote.save()
#            voteupload = PersonalVote(
#                user_id = request.user,
#                dict_json = json.dumps(PersonalVoteDict)
#            )
#            voteupload.save()
            return redirect('.')

        else:
            if sum(list(PersonalVoteDict.values())) == 5:
                messages.warning(request, '최대 5개까지 투표 가능합니다.')
                return redirect('/assess')
            else:
                PersonalVoteDict[str(assess.id)] = 1
                if PersonalVote.objects.filter(user_id=request.user).exists():
#                   PersonalVote.objects.filter(user_id=request.user)[0].delete()
                    modifyVote = PersonalVote.objects.get(id=get_object_or_404(PersonalVote, user_id=request.user).id)
                    modifyVote.user_id = request.user
                    modifyVote.dict_json = json.dumps(PersonalVoteDict)
                    modifyVote.save()
                    return redirect('.')
                else:
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
        
        n=0
        li = [assess.imagesrc1, assess.imagesrc2, assess.imagesrc3, assess.imagesrc4]
        for i in range(3):
            if li[i] != None:
                n = n+1

        context = {
            'assess': assess,
            'userVoteDict': PersonalVoteDict,
            'value': PersonalVoteDict[str(assess.id)],
            'num': len(listall),
            'present':id_list.index(assess.id) + 1,
            'prevID':prevID,
            'nextID':nextID,
            'n': n,
        }

        return render(request, 'users/Django_assess_detail.html', context)
 
