from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from pytube import YouTube
from django.conf import settings
import os 
import assemblyai as aai
import requests
import time
import json
import re
from .models import BlogPost


def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = 'YOUR_API_KEY' #ASSEMBYAI
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript.text

def gen_blog_from_transcription(text):
    
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    API_TOKEN = "YOUR_API_TOKEN" #HUGGING FACE
        
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    data = {
        "inputs": text
    }

    while True:
        response = requests.post(API_URL, headers=headers, json=data)
        if response.status_code == 503:
            error_info = response.json()
            estimated_time = error_info.get('estimated_time', 'unknown')
            print(f"Model is loading. Estimated time: {estimated_time} seconds.")
            time.sleep(5)  # Wait for 5 seconds before retrying
        elif response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code}, {response.json()}"}

def extract_summary_text(response):
    try:
        summary_text = response[0]['summary_text']
        return summary_text
    except (IndexError, KeyError) as e:
        print(f"Error extracting summary text: {e}")
        return None

@login_required  # only access to the logged users
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid Data Sent'}, status=400)
        
        # get yt title
        title = yt_title(yt_link)
        # get transcript
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': "Failed to get transcript"}, status=500)
        print(transcription)
        # use Hugging Face to generate blog
        blog_content = gen_blog_from_transcription(transcription)
        
        if not blog_content:
            return JsonResponse({'error': "Failed to generate blog content"}, status=500)
        
        # extract summary text
        summary_text = extract_summary_text(blog_content)
        print(summary_text , type(summary_text))
        if not summary_text:
            return JsonResponse({'error': "Failed to extract summary text "}, status=500)
        
        # save blog article to database 
        new_blog_article=BlogPost.objects.create(
            user=request.user,
             youtube_title = title,
             youtube_link = yt_link,
            generated_content = summary_text,
        ) 
        new_blog_article.save()
        
        # return blog article as response
        return JsonResponse({'summary_text': summary_text})
    else:
        return JsonResponse({'error': 'Invalid Request Method'}, status=405)

        

def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request,"all-blogs.html",{'blog_articles':blog_articles})


def blog_details(request, pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(request, 'blog-details.html', {'blog_article_detail': blog_article_detail})
    else:
        return redirect('/')

    


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
        
    return render(request, 'login.html')


def user_signup(request):
    if request.method == 'POST':
        username= request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        repassword=request.POST['repassword']
        if password == repassword:
            try:
                user= User.objects.create_user(username,email,password)
                user.save()
                login(request,user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
                return render(request,'signup.html' ,{'error_message':error_message})
        else:
            error_message = "password do not match"
            return render(request,'signup.html' ,{'error_message':error_message})
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')



#
