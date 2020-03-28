from flask import request, Response
from main import app
from Controllers.SpeechController import SpeechController
@app.route('/', methods=['GET'])
def index():
    sc = SpeechController()
    return sc.index(request, Response)
