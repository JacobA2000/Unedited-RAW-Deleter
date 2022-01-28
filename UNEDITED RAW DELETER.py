import os
import configparser
import tkinter as tk
from tkinter import filedialog

#READ CONFIG FILE
config = configparser.ConfigParser()
config.read('config.cfg')
beggings = config.get('FILE_BEGGINGS', 'beggings').replace(" ", "").split(',')
extensions = config.get("FILE_EXTENSIONS", "extensions").replace(" ", "").split(',')

# GET NAME OF ALL FILES IN A DIRECTORY AND STORE IN A LIST
def get_file_list(edited_files_path):
    file_list = []
    files = [ os.path.join(edited_files_path,f) for f in os.listdir(edited_files_path) if os.path.isfile(os.path.join(edited_files_path,f)) ]

    for file in files:
        for beggining in beggings:
            if beggining in file:
                file_list.append(file)
                break

    return file_list

# DELETE ALL FILES EXCEPT THOOSE WITH CERTAIN NAMES SPECIFIED IN A LIST
def get_files_to_delete(raw_files_path, file_list):
    files_to_delete = []
    for root, dirs, files in os.walk(raw_files_path):
        for file in files:
            # IF FILE IS NOT IN THE LIST, DELETE IT
            if file.lower() not in [f.lower() for f in file_list]:
                files_to_delete.append(file)

    return files_to_delete

def format_file_list(file_list):
    formatted_file_list = []

    for file in file_list:
        for index, beggining in enumerate(beggings):
            begging_index = file.find(beggining)
            if begging_index != -1:
                file = file[begging_index:]
                files = file.split('-')
                file = files[0].strip()
                file = f"{file}{extensions[index]}"
                break
        
        formatted_file_list.append(file)
    
    return formatted_file_list

def delete_files(raw_files_path, files_to_delete):
    for file in files_to_delete:
        os.remove(os.path.join(raw_files_path, file))

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    print("Please select the directory containing the edited files.")
    edited_file_path = filedialog.askdirectory()
    print ("You selected: " + edited_file_path)
    print("Please select the directory containing the raw files.")
    raw_file_path = filedialog.askdirectory()
    print ("You selected: " + raw_file_path)

    file_list = get_file_list(edited_file_path)
    f_file_list = format_file_list(file_list)
    files_to_delete = get_files_to_delete(raw_file_path, f_file_list)

    if len(files_to_delete) == 0:
        print("No files to delete.")
    else:
        print(f"The following {len(files_to_delete)} files will be deleted: ")
        for file in files_to_delete:
            print(file)

        print(f"The following {len(f_file_list)} files will be kept: ")
        for file in f_file_list:
            print(file)
            
        confirmation = input("Are you sure you want to delete all files in the directory? (y/n): ")
        if confirmation == "y":
            delete_files(raw_file_path, files_to_delete)
            print("All files have been deleted.")
        else:
            print("Exiting...")


