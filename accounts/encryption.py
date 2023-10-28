import base64,hashlib
from .models import Message

from cryptography.fernet import Fernet

def encrypt_message(key,message):
    hashed_bytes = hashlib.sha256(key.encode('utf-8')).digest()
    encoded_key = base64.urlsafe_b64encode(hashed_bytes).decode('utf-8')            

    fernet = Fernet(encoded_key)
    encMessage = fernet.encrypt(message.encode())    
    
    encMessageString = encMessage.decode('utf-8')
    
    
    msgdb= Message(content=encMessageString)
    Message.objects.all().delete()
    msgdb.save()
    
    return encMessageString
    
def decrypt_message(key,encMessage):
    hashed_bytes = hashlib.sha256(key.encode('utf-8')).digest()
    encoded_key = base64.urlsafe_b64encode(hashed_bytes).decode('utf-8')
    
    byte_message = encMessage.encode('utf-8')

    
    fernet = Fernet(encoded_key)
    decMessage = fernet.decrypt(byte_message).decode()
    return decMessage
 
