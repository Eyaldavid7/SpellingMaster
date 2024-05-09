from flask import Flask, request
from your_module import whatsapp_bot  # assuming whatsapp_bot is imported from another file

app = Flask(__name__)

@app.route('/wa')
def wa():
    return whatsapp_bot(request)

@app.route('/wasms', methods=['POST'])
def wasms():
    return whatsapp_bot(request)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)