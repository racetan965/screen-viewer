from flask import Flask, request, Response
import os

app = Flask(__name__)

latest_frame = None

@app.route('/upload', methods=['POST'])
def upload():
    global latest_frame
    latest_frame = request.data  # الصورة الخام
    return "OK", 200

@app.route('/')
def index():
    return '''
    <html>
    <body style="background:black;text-align:center;">
      <h2 style="color:white;">🎥 Live Screen Stream</h2>
      <img src="/stream" style="width:90%;border:3px solid white;"/>
    </body>
    </html>
    '''

@app.route('/stream')
def stream():
    def generate():
        global latest_frame
        while True:
            if latest_frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
