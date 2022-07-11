import os
import webbrowser


os.system('export FLASK_APP=gui')
os.system('export FLASK_ENV=development')
os.system('flask run')
webbrowser.open('http://127.0.0.1:5000')
