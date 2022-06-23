import os
from this import d
from unittest import skip
import pandas as pd
import re

def analis(reading):
    string1 = "Recommended Citation"  
    string2 = "Available at: https:"
    number = reading.find(string1)
    stopnumber = reading.find(string2)
    return number, stopnumber; 

def breaking(rujuk):
    top_row = "Name | Year | Blank | Title | Jounal"
    keys = top_row.split("|")
    match = re.search(r'\s\([0-9]+\)+\s', rujuk)
    
    if match:
        cite = re.split(r'[()""]', rujuk)
        senarai = dict(zip(keys, cite))
#        print(senarai)
        return senarai
    else:
        cite = [count, count, count, count, count]
        senarai = dict(zip(keys, cite))
        #print(rujuk)
        
        #print(senarai)
        return senarai

def wraptext(text):
    x = text.replace("\n\n", "&&&&&&&&&&&&&&&&&")
    x = x.replace("\n", " ")
    x = x.replace("&&&&&&&&&&&&&&&&&", "\n")
    x = re.sub("=+\s[a-zA-Z]+\s[0-9]+\s=+", " ", x)
    x = re.sub("=+", " ", x)
    return x

for folder in os.listdir(directory):
    my_dict = {"File_Name":[],"Citation":[]}
    citation = []
    bukasatu = os.path.join(directory, folder)
    count = 0
    
    for f_name in os.listdir(bukasatu):
        
        
        if f_name.endswith(".txt"):
            
            countfile = 0
            file1 = open(os.path.join(bukasatu, f_name), 'r', encoding="cp437")
            reading = file1.readlines()
            number = analis(reading)
            #maklmat1 = f_name + " ######### " + str(number+2)
            #print(maklmat1)
            maklumat2 = reading[number+21:stopnumber]
            sama = re.search(r'\s\([0-9]+\)+\s', maklumat2)
            
            if sama:
                my_dict["File_Name"].append(f_name)
                rujuk = reading[number+21:stopnumber]
                my_dict["Citation"].append(rujuk)
                senarai = breaking(rujuk)

                for key, value in senarai.items():
                    
                    if key in my_dict:
                        if isinstance(my_dict[key], list):
                            my_dict[key].append(value)
                        else:
                            temp_list = [my_dict[key]]
                            temp_list.append(value)
                            my_dict[key] = temp_list
                           
                            
                    else:
                        my_dict[key] = value
                        
                    
                citation.append(reading[number+21:stopnumber])
                

            else:
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" + f_name)
                top_row = "Name | Year | Blank | Title | Jounal"
                keys = top_row.split("|")
                cite = [count, count, count, count, count]
                senarai = dict(zip(keys, cite))
                count = count+1

                for key, value in senarai.items():
                    
                    if key in my_dict:
                        if isinstance(my_dict[key], list):
                            my_dict[key].append(value)
                        else:
                            temp_list = [my_dict[key]]
                            temp_list.append(value)
                            my_dict[key] = temp_list
                           
                            
                    else:
                        my_dict[key] = value
                print(senarai)
            file1.close()
            countfile = countfile+1
            print(countfile)

    print(len("File_Name"),len("Citation"), len("Title"))


    df = pd.DataFrame(my_dict)
    print("Given Dataframe :\n", df)
    
    output_filename = r"E:\Belajar Master in Maritime Technology\GITHUB HUZAIFAH16\ken-batcher-pp-ocr\testfolder\summary " + folder + ".csv"
    print(output_filename)
    df.to_csv(output_filename, index = False, header=True)
