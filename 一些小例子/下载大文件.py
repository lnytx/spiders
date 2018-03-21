'''
Created on 2017年5月10日

@author: ning.lin
'''
from django.http.response import HttpResponse


def bigFileView(request):
    # do something...

    def readFile(fn, buf_size=262144):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    file_name = "big_file.txt"
    response = HttpResponse(readFile(file_name))
    return response
if __name__=='__main__':
    request=request.get
    bigFileView(request)
    