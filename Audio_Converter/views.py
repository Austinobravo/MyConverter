from django.shortcuts import render,redirect
from .models import *
import pytube
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from os.path import exists
import time
import os
import re
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.
#Creating home view
def home(request):
    '''
    form = FileForm
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.cleaned_data.get('music')
            db_video = File(music=video)
            db_video.save()
            local_video = File.objects.filter().last()
            print(video, 'form is valid')
            
            convert_video =  VideoFileClip(str(local_video))

            print(convert_video, 'form is very valid')

            #Converting to an audio

            audio = convert_video.audio
            audio.write_audiofile("❤Converter.mp3")
            

    context = {
        'form': form
    }
'''
    return render(request,'index.html')
# Deleting Older files View
def clearolderfiles(path):
    deletepath = "media\\"+path    
    if exists(deletepath):          
        for folder in os.listdir(deletepath):                                
            modifiedtime=os.path.getmtime(os.path.abspath(deletepath+"\\"+folder))          
            if time.time()-modifiedtime > 300:
                for file in os.listdir(deletepath+"\\"+folder):
                    os.remove(os.path.abspath(deletepath+"\\"+folder+"\\"+file))
                os.rmdir(os.path.abspath(deletepath+"\\"+folder))  
       
#Details View
def details(request):
    if request.method == 'POST':
        Links = request.POST.get('link')
        if Links:
            link = Link(link=Links)
            link.save()
        last_link= Link.objects.filter().last()      
        try:
            #Checking if the video can be Processed.
            Details = YouTube(str(last_link)).check_availability()
            #Getting the youtube details
            Details = YouTube(str(last_link))

        except VideoUnavailable:
            last_link.delete()
            messages.info(request, "This link is unavailable.")
            return redirect('home')

        except :
            last_link.delete()
            messages.info(request, "This link doesn't exists or is broken.")
            return redirect('home')

        
        #Download the mp3 file.
        if request.POST.get('submit') == 'downloadmp3':
            last_link= Link.objects.filter().last()
            #Clear old file and create a newone
            clearolderfiles("audiofiles")    
            # url input from user    
            #print("URL>>"+request.POST["address"])
            my_new_path ="media\\audiofiles\\"+re.sub('[^a-zA-Z0-9 \n\.]', '', str(last_link))
            if exists(my_new_path):          
                for file in os.listdir(my_new_path):
                    if file.endswith(".mp3"):
                            audiofile = open(my_new_path+"\\"+file, "rb").read() 
                            response = HttpResponse(audiofile, content_type='audio/mpeg')
                            response['Content-Disposition'] = 'attachment; filename=' + file
            else:
            #Start Conversion
                Mp3 = YouTube(str(last_link))
                # extract only audio
                video = Mp3.streams.filter(only_audio=True).first()

                # download the file        
                out_file = video.download(output_path=my_new_path)
                # save the file
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'        
                os.rename(out_file, new_file)
                # result of success
                # print(yt.title + " has been successfully downloaded.")
                # last_link.delete()
                # messages.success(request, f'Your song {Details.title} has been downloaded')
                
                for file in os.listdir(my_new_path):
                    if file.endswith(".mp3"):
                        audiofile = open(my_new_path+"\\"+file, "rb").read() 
                        response = HttpResponse(audiofile, content_type='audio/mpeg')
                        response['Content-Disposition'] = 'attachment; filename=' + file
            return response
        #Download the mp4 file.    
        elif request.POST.get('submit') == 'downloadmp4':
            last_link= Link.objects.filter().last()

            #Clearing old files and creating new ones
            clearolderfiles("videofiles")
            my_new_path ="media\\videofiles\\"+re.sub('[^a-zA-Z0-9 \n\.]', '', str(last_link))
            if exists(my_new_path):          
                for file in os.listdir(my_new_path):
                    if file.endswith(".mp4"):
                            audiofile = open(my_new_path+"\\"+file, "rb").read() 
                            response = HttpResponse(audiofile, content_type='application/vnd.mp4')
                            response['Content-Disposition'] = 'attachment; filename=' + file
            else:
                #Start File Processing.
                Mp4 = YouTube(str(last_link))
                video = Mp4.streams.get_highest_resolution()

                # download the file        
                out_file = video.download(output_path=my_new_path)
                for file in os.listdir(my_new_path):
                    if file.endswith(".mp4"):
                            audiofile = open(my_new_path+"\\"+file, "rb").read() 
                            response = HttpResponse(audiofile, content_type='application/vnd.mp4')
                            response['Content-Disposition'] = 'attachment; filename=' + file
            return response



        context = {
                'link': Links,
                'title':Details.title,
                'author':Details.author,
                'date': Details.publish_date,
                'duration':str(Details.length),
                'image':Details.thumbnail_url,
                'description':Details.description,
                'views':str(Details.views),
                'age':str(Details.age_restricted),
                'video_id':str(Details.video_id)
            }
          

        return render(request, 'details.html', context)
    else:
        return render(request, 'details.html')




