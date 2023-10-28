from django.shortcuts import render
import time
from numpy import matrix
from math import pow, sqrt
from random import randint
import sys, argparse
from accounts.quantum_channel import *
from .models import secret_keys,Message
from .encryption import encrypt_message, decrypt_message
import json
from django.http import JsonResponse
 
idxValue = 0

def func(request):
    global idxValue
    ret = list()
    N = 128
    key = secret_keys(sender_key = "" , receiver_key = "")
    key.save()
    idx = key.id
    idxValue = idx
    key = ""
    for i in range (N):
        print ("############# {0} #############".format(str(i)))
        ret.append(QKD(16,idx,verbose = True ,eve_present = True))
        print ("###############################".format(str(i)))
    secret_key = secret_keys.objects.filter(id= idx)
    print("sender key :"+secret_key[0].sender_key)
    print("receiver_key: "+secret_key[0].receiver_key)
    
    t = "{0:.2f}".format(float(ret.count(True))*100.0/float(N))
    u = "{0:.2f}".format(float(ret.count(False))*100.0/float(N))
    print ("True: {0} <{1}%>".format(ret.count(True),str(t)))
    print ("False: {0} <{1}%>".format(ret.count(False),str(u)))
    
    
    enc = encrypt_message(secret_key[0].sender_key,"Hello World!")
    dec = decrypt_message(secret_key[0].receiver_key,enc)
    return render(request,'accounts/demo.html', {'key' : secret_key[0], 'dec' : dec, 'enc' : enc})



def receive_message(request):
    received_messages = Message.objects.all()
    
    # for message in received_messages:
    #     message.content
    # print(received_messages[0].content)
    
    
    
    
    secret_key = secret_keys.objects.filter(id= idxValue)
    original_str = []
    for message in received_messages:
        print(message.content)
        original_str.append(decrypt_message(secret_key[0].sender_key , message.content))
    
    print(original_str)
    
    return render(request, 'accounts/receive_message.html', {'received_messages': original_str[0]})

def send_message(request):
    global idxValue
    if request.method == 'POST':

        # Handle form submission and message sending logic here
        # For example, you can save the message to a database
        data = json.loads(request.body)

        message = data.get("message", "")

        print("Sender mEssage",message)
        secret_key = secret_keys.objects.filter(id= idxValue)
        
        encrypt_message(secret_key[0].sender_key ,message)
        # Save the message to the database or perform any other desired action
        # Redirect to a success page or the send_message page
        return render(request, 'accounts/send_message.html')
    else:
        return render(request, 'accounts/send_message.html')
