from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Essa vai ser a Homepage da Página'

@app.route('/contato')
def contato():
    return 'Qualquer dúvida mande um e-mail para contato@tanana.com'

if __name__ == '__main__':
    app.run(debug=True)