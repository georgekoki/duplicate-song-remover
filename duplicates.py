from email.mime import base
import Levenshtein as lev
import os
from os import path
import sys
import eyed3

target_path = input("Folder path:\n")
sensitivity = input("Sensitivity (0-10):\n")

if(not path.exists(target_path) or not sensitivity.isdigit()):
    print("Usage:\nFolder path: The folder you want to check for duplicates\n" + 
    "Sensitivity: A value between 0 and 10 on how similar the files have to be. Higher is more.")
    exit()

sensitivity = int(sensitivity)

for path, subdirs, files in os.walk(target_path):
    for name in files:
        full_path = os.path.join(path, name)
        for path_scan, subdirs_scan, files_scan in os.walk(target_path):
            for name_scan in files_scan:
                full_path_scan = os.path.join(path_scan, name_scan)
                if(lev.distance(name[:-4], name_scan[:-4]) <= sensitivity and 
                full_path != full_path_scan):
                    base_file = eyed3.load(full_path)
                    scan_file = eyed3.load(full_path_scan)
                    
                    if(hasattr(base_file, 'tag') and hasattr(scan_file, 'tag')):
                        if(lev.distance(base_file.tag.artist, scan_file.tag.artist) <= sensitivity and
                        lev.distance(base_file.tag.title, scan_file.tag.title) <= sensitivity ):
                            print(base_file.tag.artist + " - " + base_file.tag.title)
                            print("1: " + full_path + "\n" + "2: " + full_path_scan + "\n")
                            choice = input("Delete: ")
                            if(choice == "1"):
                                os.remove(full_path)
                            if(choice == "2"):
                                os.remove(full_path_scan)
                    else:
                        print(base_file.tag.artist + " - " + base_file.tag.title)
                        print("1: " + full_path + "\n" + "2: " + full_path_scan + "\n")
                        choice = input("Delete: ")
                        if(choice == "1"):
                            os.remove(full_path)
                        if(choice == "2"):
                            os.remove(full_path_scan)
                            
input("\nDone\nPress any key to exit this window...\n")
