import os
import requests
import json
import uuid
import shortuuid
import hashlib
from datetime import date
from .model import add_new_image
from .model import get_images
from .model import get_all_messages
from .model import get_messages
from .model import add_new_message
from .model import current_message_exist
from .model import update_message
from twilio.rest import Client
from django.http import JsonResponse
from django import forms
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button
from tethys_sdk.workspaces import app_workspace
from twilio.twiml.messaging_response import MessagingResponse




@csrf_exempt
def bot(request):
    # get message body
    incoming_msg = request.POST.get('Body', '').lower()
    # get Latitude and Longitude
    lat, lon = request.POST.get('Latitude', 1), request.POST.get('Longitude', 1)
    # get phone number
    phone_number = request.POST.get('From', '')
    # make hash phone number
    p_i = hashlib.md5(phone_number.encode()).hexdigest()
    # check if it is a first message 
    num_media = int(request.POST.get('NumMedia', 0))
    media = request.POST.get('MediaContentType0', '')
    # mesage variables
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    # check if message has data 
    if incoming_msg or lat != 1 or num_media > 0:
        #Future variables
        title = ""
        owner = ""
        event = ""
        path = ""
        # verify the point of the conversation
        first = False
        f_m = True
        m_id, title, event, owner = current_message_exist(p_i, title, event, owner)
        if m_id == None :
            first = True
            m_id = uuid.uuid4().hex
        #If there are any files save them on the path defined
        if num_media > 0:
            if media.startswith('image/'):
                extension = media.split('/')[1]
                filedesc = shortuuid.uuid()+ "."+ extension
                file_controller(request, filedesc, m_id)
        #Check the conditional logic of the conversation script
        if num_media > 0:
            msg.body('Thank you! You may now upload additional images. Enter "done" when finished.')
            responded = True  
        elif lat != 1 and lon != 1:
            msg.body('Thank you! Please provide a short descriptive title for the info you are reporting.')
            responded = True
        elif 'hello' in incoming_msg:
            quote = 'Welcome to SERVIR flood monitoring! We are collecting first-person accounts of flooding. Please enter the location of the info you wish to report by clicking on the “+” to the left of the text entry box in Whatsapp'
            msg.body(quote)
            responded = True
        elif 'done' in incoming_msg:
            msg.body('Thank you for providing information for this flooding event.')
            f_m = False
            responded = True
        elif title == "" and  event == "" and owner == "" and not first:
            msg.body('Thank you! Please provide your name.')
            title = incoming_msg
            responded = True
            print('title')
        elif title != "" and event == "" and owner == "" and not first:
            msg.body('Enter the info you wish to report in the chat. You may upload images, video or text. Enter "done" when finished.')
            owner = incoming_msg
            responded = True
            print('owner')
        elif title != "" and event == "" and owner != "" and not first:
            msg.body('Thank you! You may now upload additional images. Enter "done" when finished.')
            event = incoming_msg
            responded = True
        if not responded:
            msg.body('I can not understand please send location, image or type "done"')
        #Keeps track of the conversation use prints to debug
        if first == True:
            # print("added new")
            add_new_message(p_i, f_m, m_id, lat, lon, title, owner, event, date.today())
        elif num_media == 0:
            # print("update")
            update_message(p_i, m_id, f_m, lat, lon, title, owner, event)

    return HttpResponse(resp, content_type='application/xml')

@app_workspace
def file_controller(request, name, m_id, app_workspace):
    #Save file on the both directories they need to be 
    new_file_path = os.path.join(app_workspace.path, name)
    current_path = os.path.dirname(os.path.realpath(__file__)) 
    public_path = os.path.join(current_path + '/public/images/', name)
    with open(new_file_path, 'wb') as a_file:
        a_file.write(requests.get(request.POST.get('MediaUrl0')).content)
    with open(public_path, 'wb') as a_file:
        a_file.write(requests.get(request.POST.get('MediaUrl0')).content)
    add_new_image(m_id, name)

@login_required()
def search(request):
    #Search params
    stype = request.GET.get('s_type', '')
    value = request.GET.get('search', '')
    messages = None
    if stype == '':
        messages = get_all_messages()
    else:
        messages = get_messages(stype, "%{}%".format(value))
    
    results = []
    #Format data 
    for m in messages:
        dict_data = {
            'title'  : m.title,
            'lat' : m.latitude,
            'longit' : m.longitude,
            'name' : m.owner,
            'desc' : m.event,
            'media' : serialize_images(m.message_id),
        }
        results.append(dict_data)
    
    return_obj = {}
    return_obj['message'] = json.dumps(results)
    return_obj['status'] = True
    return JsonResponse(return_obj)

def serialize_images(m_id):
    images = get_images(m_id)
    mediaSerial = []
    for image in images:
        mediaSerial.append(image.path)
    return ",".join(mediaSerial)

def home(request):
    """
    Controller for the app home page.
    """
    save_button = Button(
        
    )

    edit_button = Button(
   
    )

    remove_button = Button(
    
    )

    previous_button = Button(
     
    )

    next_button = Button(
     
    )

    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button
    }

    return render(request, 'whats_app/home.html', context)