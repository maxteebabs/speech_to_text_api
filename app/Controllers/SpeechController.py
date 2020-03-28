from flask import jsonify,json
from werkzeug.utils import secure_filename
from Helpers.SpeechHelper import SpeechHelper
import os
from Helpers.GoogleCloudStorage import GoogleCloudStorage
class SpeechController:
    speechHelper = None
    googleCloudStorage = None
    def __init__(self):
        self.speechHelper = SpeechHelper()
        self.googleCloudStorage = GoogleCloudStorage()
    def index(self, request, response):
        responseText = ""
        http_code = 201
        try:
            upload_dir = "./audio"
            # app.config[‘MAX_CONTENT_PATH’]
            audio = request.files['audio']
            # print() //bytes            
            if audio.filename == '':
                raise ValueError("Please ensure you upload a file")
            
            size = os.path.getsize(audio.filename)
            if(size > 100000):
                raise ValueError("Audio file size is too large")

            if(audio.content_type not in ["audio/mpeg"]):
                raise ValueError("File upload must be an audio format")
            #save the file into google cloud
            filepath = self.googleCloudStorage.store(audio.filename,audio.content_type)

            # filepath = upload_dir+'/'+secure_filename(audio.filename)
            # audio.save(filepath)
            responseText = self.speechHelper.convertToText(filepath)
            if(responseText):
                # lets delete the file afterwards
                self.googleCloudStorage.delete_file(audio.filename)
        except Exception as err:
            responseText = str(err)
            http_code = 400
        finally:
            jsonR = json.dumps({
                "message" : responseText
            })
            return response(jsonR, status=http_code, mimetype='application/json')
        
        
    
        
