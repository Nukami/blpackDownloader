"""
Author: Nukami
Blog: blog.sailark.com
Date: 2019/7/31
Description: A downloader for blpack.com to download documents on wenku.baidu.com easily
Usage:
python blpack.py billing
python blpack.py [url] [dest]
"""

import urllib.request as request
import urllib.parse as parse
import json
import os
import sys

user = "403526350"
password = "459349"


def http_request(url, payload=''):
    request_header = {
                      'User-Agent': 'Mozilla/5.0',
                      }
    rq = request.Request(url) if payload == '' else request.Request(url, data=parse.urlencode(payload).encode('utf-8'))
    for tmp in request_header:
        rq.add_header(tmp, request_header[tmp])
    f = request.urlopen(rq)
    header = f.info()
    return f.read(), header


def get_nocode_url(doc_url):
    payload = {'usrname': user,
               'usrpass': password,
               'docinfo': doc_url,
               'taskid': 'up_down_doc1'
               }
    resp, header = http_request("http://www.blpack.com/post.php", payload)
    resp = resp.decode("utf8")
    result = json.loads(resp)
    return result['url']


def get_vid(url):
    resp, header = http_request(url)
    resp = resp.decode("utf8")
    left_flag = 'value="'
    left_index = resp.find(left_flag) + len(left_flag)
    return resp[left_index:left_index + 32]


def get_dlink(vid):
    payload = {'vid': vid,
               'taskid': 'directDown'
               }
    resp, header = http_request("http://www.blpack.com/downdoc.php", payload)
    resp = resp.decode("utf8")
    result = json.loads(resp)
    return result['dlink'].replace("\\/", "/")


def get_file_name(header):
    desp = header['Content-Disposition']
    left_flag = 'filename="'
    right_flag = '";'
    left_index = desp.find(left_flag)
    right_index = desp.find(right_flag, left_index)
    return parse.unquote(desp[left_index+len(left_flag):right_index])


def save_to(content, path):
    f = open(path, 'wb+')
    f.write(content)
    f.flush()
    f.close()


def get_desktop():
    return os.path.join(os.path.expanduser("~"), 'Desktop')


def download(url, dest=""):
    dest = dest if dest != "" else get_desktop()
    nocode = get_nocode_url(url)
    print("nocode url: %s\n" % nocode)
    vid = get_vid(nocode)
    print("vid: %s\n" % vid)
    dlink = get_dlink(vid)
    print("download link: %s\n" % dlink)
    content, header = http_request(dlink)
    file_name = get_file_name(header)
    file_path = "%s\\%s" % (dest, file_name)
    print("Document will be saved to %s, length %s\n" % (file_path, len(content)))
    save_to(content, file_path)
    return file_name


def get_balance():
    payload = {'usrname': user,
               'usrpass': password,
               'taskid': 'getwealth'
               }
    resp, header = http_request("http://www.blpack.com/post.php", payload)
    resp = resp.decode("utf8")
    result = json.loads(resp)
    return result['wealth']


if __name__ == "__main__":
    echo = '''
    blpack.com Downloader by Nukami, 2019/7/31
    1. Set your blpack.com account in .py file,
    2. Run "python blpack.py [ balance | | url, directory ]"
    '''
    print(echo)
    args = sys.argv
    app = "" if len(args) <= 2 else args[2]
    cmd = args[1] if len(args) > 1 else 'balance'
    if cmd == 'balance':
        print("Balance: %s\n" % get_balance())
    else:
        download(cmd, app)
        print("Job done!\n")

