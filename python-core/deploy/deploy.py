# It is supposed to you already have a default xr server available in the $XR_SERVER_FOLDER folder.
# This script will deploy it's custom files into the xr server


import os
import shutil

print "[!]   Deploying files..."

# Destination
XR_SERVER_PATH = '/home/igor/instagib/xr_server/'

current_dir_path = os.path.dirname(os.path.realpath(__file__))
src = current_dir_path + '/../server/'
print "- src_root: " + src
print "- dst_root: " + XR_SERVER_PATH


def copy_files(src_path, dst_path):
    if not os.path.exists(os.path.dirname(dst_path)):
        try:
            os.makedirs(dst_path)
        except:
            pass
    files = [f for f in os.listdir(src_path) if os.path.isfile(os.path.join(src_path, f))]
    for f in files:
        shutil.copy(src_path + f, dst_path)


def copy_one(src_path, dst_path):
    if not os.path.exists(os.path.dirname(dst_path)):
        try:
            os.makedirs(dst_path)
        except:
            pass
    shutil.copy(src_path, dst_path)

print "  deploying: /server/"
copy_files(src, XR_SERVER_PATH + 'game/python/')

print "  deploying: /server/configs/"
copy_one(src + '/configs/XR_admin.cfg', XR_SERVER_PATH + 'game/')
copy_one(src + '/configs/Passwords.cfg', XR_SERVER_PATH + 'game/')
copy_one(src + '/configs/Instagib.cfg', XR_SERVER_PATH + 'game/script/instagib/')

print "  deploying: /server/triggers/"
copy_files(src + '/triggers/', XR_SERVER_PATH + 'game/python/triggers/')

print "[!]   Finished deploying"
