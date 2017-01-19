# ---------------------------------------------------------------------------
#           Name: le_assets.py
#         Author: Anthony Beaucamp (aka Mohican)
#  Last Modified: 10/23/2011
#    Description: Assets loading/saving manager
# ---------------------------------------------------------------------------

import core, gui
import os, shutil, zipfile

def refresh():
    # Clear scrollbuffer
    core.CommandExec('o_scrollbuffer clear assets_sb')

    # List files in "/_assets_/"
    tempdir = os.path.join(os.getcwd(), '_assets_')
    for path, names, filenames in os.walk(tempdir):
        for filename in filenames:
            core.CommandExec('o_scrollbuffer print assets_sb "%s"' % (filename))
            
def importFile():
    # Does file exist?
    filepath = core.CvarGetString('le_asset_import')
    if not os.path.isfile(filepath):
        return

    # Make sure there is an /_assets_/ directory
    tempdir = os.path.join(os.getcwd(), '_assets_')
    if not os.path.isdir(tempdir):
        os.makedirs(tempdir)
    
    # Copy file into it
    (path, file) = os.path.split(filepath)
    shutil.copyfile(filepath, os.path.join(tempdir, file))
    
    # Refresh GUI
    refresh()
    
def exportFile():
    # Does file exist?
    file = core.CvarGetString('_assets_sb_variable')
    tempdir = os.path.join(os.getcwd(), '_assets_')
    if not os.path.isfile(os.path.join(tempdir, file)):
        return

    # Copy file to export folder
    filepath = core.CvarGetString('le_asset_export')
    shutil.copyfile(os.path.join(tempdir, file), os.path.join(filepath, file))
    
def remove():
    # Delete currently selected file 
    file = core.CvarGetString('_assets_sb_variable')
    tempdir = os.path.join(os.getcwd(), '_assets_')
    os.remove(os.path.join(tempdir, file))
    
    # Refresh GUI
    refresh()


# -------------------------------
# Called directly by Silverback
# -------------------------------
def deflate(map_name):
    # Prepare file paths
    map_path = os.path.join(os.getcwd(), '../game/world/' + map_name + '.s2z')    
    tempdir = os.path.join(os.getcwd(), '_assets_')
    
    # Empty any existing dir /_assets_/
    if os.path.isdir(tempdir):
        shutil.rmtree(tempdir)
    os.makedirs(tempdir)
        
    # Unzip assets
    map_zip = zipfile.ZipFile(map_path, "r", zipfile.ZIP_DEFLATED)
    for member in map_zip.namelist():
        # only keep /assets/
        if '/assets/' not in member:
            continue
        
        # skip directories
        filename = os.path.basename(member)
        if not filename:
            continue

        # copy file (taken from zipfile's extract)
        source = map_zip.open(member)
        target = file(os.path.join(tempdir, filename), "wb")
        shutil.copyfileobj(source, target)
        source.close()
        target.close()

# -------------------------------
# Called directly by Silverback
# -------------------------------
def inflate(map_name):
    # Prepare file paths
    map_path = os.path.join(os.getcwd(), '../game/world/' + map_name + '.s2z')    
    tempdir = os.path.join(os.getcwd(), '_assets_')
    reldir = 'world/' + map_name + '/assets'

    # Simply re-zip files from /_assets_/
    map_zip = zipfile.ZipFile(map_path, "a", zipfile.ZIP_DEFLATED)
    for path, names, filenames in os.walk(tempdir):
        for filename in filenames:
            absolute_path = os.path.join(path,filename)
            relative_path = os.path.join(reldir,filename)
            map_zip.write(absolute_path, relative_path)
    map_zip.close()
