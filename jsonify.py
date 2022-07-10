import json
import re

"""---------------------------------
            Print Dictionary 
----------------------------------"""
def dev_print_dict_n(dict):
    for k,v in dict.items():
        print(k,':',v)

"""---------------------------------
        Converts list to Json
----------------------------------"""  
def jsonify(entry):
    # Splits String into list indexted by deliminator ',' except for in quotes 
    # (?<=...) is a "positive lookbehind assertion". It causes pattern (in this case, just a comma, ",") to match commas in the string only if they are preceded by the pattern given by [\",], which means "either a quotation mark or a comma".
    # (?=...) is a "positive lookahead assertion". It causes pattern to match commas in the string only if they are followed by the pattern specified as (again, [\",]: either a quotation mark or a comma).
    # Since both of these assertions must be satisfied for the pattern to match, it will still work correctly if any of your 'objects' begin or end with commas as well. 
    return re.split(r'(?<=[\",]),(?=[\",])', entry) 

"""---------------------------------
    Converts lists to Dictionary
----------------------------------""" 
def dictionify(value_list,field_list):
    json_dict={}
    #unique name for each dictionary entry 
    id=0
    for value in value_list:
        id_dict={}
        id+=1
        json_dict[id]=id_dict
        for field in field_list:
            formats_last_entry(field_list,field,value_list,value)
            id_dict[field.strip('\"')]=value[field_list.index(field)].strip('\"')
    return json_dict

"""---------------------------------
        Formats Last Entry
----------------------------------""" 
def formats_last_entry(field_list, field_value,value_list, value):
    field_value_index=field_list.index(field_value)
    value_index = value_list.index(value)
    #some data in xml file is missing this checks for indexError in that case
    try:
       entry = value_list[value_index][field_value_index]
       #strips return carriage from original xml data 
       value_list[value_index][field_value_index] = entry.strip('&#xd;\n')
    except IndexError:
        #append null data to fill index that is missing
        value_list[value_index].append('')

__name__='__main__'

#parse response into list 
with open('responseLine.txt')as f:
    lines = f.readlines()

#parse feild into list
field_list = lines[0].split(',')
#manualy strip the invalid hex char at end of field value
field_list[-1]=field_list[-1].strip('&#xd;\n')

#parse values into list 
value_list_1d = []
for l in lines[1:]:
    value_list_1d.append(l)
#split list into individual values     
value_list=[]
for entry in value_list_1d:
    json_obj = jsonify(entry)
    value_list.append(json_obj)

#create dictionary with field and values 
json_dict=dictionify(value_list,field_list)

# dev_print_dict_n(json_dict)

#convert dictionary into json dump to output
print(json.dumps(json_dict))




