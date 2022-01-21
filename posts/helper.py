from django.core.files.storage import FileSystemStorage
import os


def check_route(current_route, previousRoute, request):
    if previousRoute is not None:
        splittedRoute = previousRoute.split('/')
        if (splittedRoute[-2] == 'create'):
            if (splittedRoute[-3] != current_route):
                request.session["create_update_confirm_page_flag"] = False
        elif (splittedRoute[-2] == 'update'):
            if (splittedRoute[-4] != current_route):
                request.session["create_update_confirm_page_flag"] = False
        else:
            request.session["create_update_confirm_page_flag"] = False
    else:
        request.session["create_update_confirm_page_flag"] = False

def save_temp(f):
    with open('posts/static/temp/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return f.name

def handle_uploaded_file(file_name):
    with open('posts/static/temp/' + file_name, 'rb') as tmp:
        img_str = tmp.read()
        with open('media/'+file_name, 'wb+') as upload:
            upload.write(img_str)

def remove_temp(f, root_dir):
    if (root_dir and f):
        os.unlink(root_dir+'\\static\\temp\\' + f)