import datetime


def yearCopyRight(request):
    return {'yearCopyRight': datetime.datetime.now().year}
