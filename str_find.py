import os
text = input('The key word:')
path = input('The path: ')
def searchText (path):
    os.chdir(path)
    files = os.listdir()
    for fil in files :
        abs_path = os.path.abspath(fil)
        #print(abs_path)
        if os.path.isdir(abs_path):
           searchText(abs_path)
           if os.path.isfile(abs_path):
              with open(fil,'r',encoding='utf-8') as f :
                   #print(f.read())
                   if text in f.read():
                      final_path = os.path.abspath(fil)
                      print(f'the {text} found in this path {final_path}')
                   else:
                       print(f'Not found in {abs_path}')
                       pass
searchText(path)
