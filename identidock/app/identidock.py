from __future__ import print_function
import sys
from flask import Flask, Response, request # https://pypi.org/project/Flask/1.0.2/
import requests
import hashlib
import redis
#import html

stdout=sys.stdout
print("DEBUG C:Start identidock.py", file=stdout)
stdout.flush()

app = Flask(__name__)
cache = redis.StrictRedis( host='redis_cont', port=6379, db=0)
salt = "unique_salt"

default_name = 'Joe Bloggs'

@app.route('/', methods=['GET', 'POST'])
def mainpage():

    name = default_name

    if request.method == 'POST':
        name = escape( request.form['name'], quote=True)

    salted_name = salt + name
    name_hash = hashlib.sha256( salted_name.encode()).hexdigest()

    header = '<html><head><title>Identidock</title></head><body>'
    body = '''<form method="POST">
            Hello <input type="text" name="name" value="{0}">
            <input type="submit" value="submit">
            </form>
            <p>You look like a B:
            <img src="/monster/{1}"/>
            <p>name/hash:{0}/{1}
            '''.format(name, name_hash)
    footer = '</body></html>'
    return header + body + footer


@app.route('/monster/<name>')
def get_identicon( name ):

    name = escape( name, quote=True) #
    image = cache.get( name )
    if image is None:
        print("Cache miss", file=stdout)
        stdout.flush()
        r = requests.get('http://dnmonster:8080/monster/' + name + '?size=80')
        image = r.content
        cache.set( name, image)
    else:
        print("Cache used.", file=stdout)
        stdout.flush()

    return Response( image, mimetype='image/png')

def escape(str, quote=True):
    # https://wiki.python.org/moin/EscapingHtml
    import cgi
    return cgi.escape(str, quote=True)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

