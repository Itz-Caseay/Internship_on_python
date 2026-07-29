import os
import shutil

path = input("Enter Path: ")
files = os.listdir(path)

for file in files:
    