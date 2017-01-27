from cryptography.fernet import Fernet
import base64


SECRET_KEY = base64.urlsafe_b64decode(Fernet.generate_key())
SECURITY_KEY = 'what is love? Baby, dont hurt me, dont hurt me no more'
