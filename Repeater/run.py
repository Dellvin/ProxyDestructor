import os
import socket
import ssl
import subprocess


def get_decision():
    print(' To view request''s list enter: "l"')
    print(' To view/modify certain request enter: "v {%filename%}"')
    print(' To resend certain request enter: "r {%filename%}"')
    print(' To mine params of certain GET request enter: "m {%filename%}"')
    print(' To exit enter: "q"')
    decision = input()
    return decision


def get_list():
    for root, dirs, files in os.walk("./static"):
        for filename in files:
            print("     ->" + filename)


def view(file):
    subprocess.call(['nano', file])


def get_file_name(command):
    x = command.split()
    return x[len(x) - 1]


def make_https_request(host, data):
    port = 443
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        ssl_sock = ssl.wrap_socket(s)
        ssl_sock.connect((host, port))
        ssl_sock.sendall(data.encode())
        data = ssl_sock.recv(1024)

    return data.decode()


def make_http_request(host, data):
    port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        ssl_sock = s
        ssl_sock.connect((host, port))
        ssl_sock.sendall(data.encode())
        data = ssl_sock.recv(1024)

    return data.decode()


def resend(file):
    f = open(file, 'r')
    content = f.read()
    data = ''
    req = get_request_from_file(content)
    if content.find('HTTPS') != -1:
        data = make_https_request(get_host_from_file(content), req)
    else:
        print("Request\n\n" + req + "Response\n\n")
        data = make_http_request(get_host_from_file(content), req)
    print(data)


def mine(file: str):
    f = open(file, 'r')
    content = f.read()
    content = get_request_from_file(content)
    if not is_get_request(content):
        return 'error: request is not GET'
    else:
        f = open('../conf/params')
        line = f.readline()
        while line:
            r=replace_param(line, content)
            if r==-1:
                return 'There no url args in request'
            if content.find('HTTPS') != -1:
                data = make_https_request(get_host_from_file(content), r)
            else:
                data = make_http_request(get_host_from_file(content), r)
            if data.find(line) !=-1:
                print("hacked with:", line)
            line = f.readline()
        f.close()


def replace_param(param: str, content: str):
    pos = content.find('=')
    if pos == -1:
        return -1
    end = content.find(' ', pos)
    if end == -1:
        return -1

    content = content[:pos + 1] + content[end:]

    return content[:pos + 1] + param + content[pos + 1:]


def get_url(content: str):
    pos = content.find('/') + 1
    url = ''
    while content[pos] != ' ':
        url += content[pos]
        pos += 1
    return url


def is_get_request(content: str):
    if content.find('GET') == -1:
        return False
    else:
        return True


def get_host_from_file(content: str):
    pos = content.find('//') + 2
    host = ''
    while content[pos] != '/':
        host += content[pos]
        pos += 1
    return host


def get_request_from_file(content: str):
    pos = content.find('<{[') + 3
    req = ''
    while content[pos] != ']' and content[pos + 1] != '}' and content[pos + 2] != '>':
        req += content[pos]
        pos += 1
    return req


# main

print("Welcome to hacker_master!")
while True:
    r = get_decision()
    if r == 'q':
        exit(0)
    if r == 'l':
        get_list()
    if r[0] == 'v':
        view('./static/' + get_file_name(r))
    if r[0] == 'r':
        resend('./static/' + get_file_name(r))
    if r[0] == 'm':
        mine('./static/' + get_file_name(r))
    else:
        print('unknown command')

# m 1614774258_GET_www.example.org.txt
