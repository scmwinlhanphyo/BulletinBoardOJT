from django.conf import settings
import os

def check_route(current_route, previousRoute, request):
    """
    check route for confirm and create page.
    Param current_route
    """
    if previousRoute is not None:
        splittedRoute = previousRoute.split("/")
        if (splittedRoute[-2] == "create"):
            if (splittedRoute[-3] != current_route):
                request.session["create_update_confirm_page_flag"] = False
        elif (splittedRoute[-2] == "update"):
            if (splittedRoute[-4] != current_route):
                print('session false')
                request.session["create_update_confirm_page_flag"] = False

def save_temp(f):
    """
    save temp file in temp folder.
    Param f request file.
    Return file name.
    """
    with open("media/temp/"+f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return f.name

def handle_uploaded_file(file_name):
    """
    save file to media folder from temp folder.
    Param file_name
    """
    with open("media/temp/" + file_name, "rb") as tmp:
        img_str = tmp.read()
        with open("media/"+file_name, "wb+") as upload:
            upload.write(img_str)

def remove_temp(f):
    """
    remove file from temp folder.
    f filename, root_dir Project Root Directory.
    """
    if (f):
        os.unlink(str(settings.BASE_DIR)+"\\media\\temp\\" + f)