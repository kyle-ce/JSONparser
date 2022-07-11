import json
import re

"""---------------------------------
            Print Dictionary 
----------------------------------"""
def dev_print_dict_n(dict):
    for k,v in dict.items():
        print(k,':',v)

"""---------------------------------
       Parse String into List 
----------------------------------"""  
def parse_string(entry):
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
            #strip quotes from data so JSON dumps cleanly  
            id_dict[field.strip('\"')]=value[field_list.index(field)].strip('\"')
    return json_dict

"""---------------------------------
        Formats Null Data 
----------------------------------""" 
def formats_null_data(value):
    LAST_ENTRY=26
    #some data in xml file is missing this checks for indexError in that case
    try:
       entry = value[LAST_ENTRY]
    except IndexError:
        #append null data to fill index that is missing
        value.append('')

"""---------------------------------
        JSON Formater 
----------------------------------""" 
def json_formater(value):
    SUBMITTED_AMOUNT_INDEX=25
    LINE_ITEM_INVOICE_ID_INDEX=26
    for row in value:
        #remove return carriage from last value entry 
        row[-1]=row[-1].strip('(&#xd;\n)||(,&#xd;\n)')
        #add null data
        formats_null_data(row)
        

__name__='__main__'
with open('responseLine.txt')as f:
    lines = f.readlines()
'''---------------------------------
parse file into two lists: field and value
---------------------------------'''
field_list = lines[0].split(',')
#manualy strip the invalid hex char at end of field value
field_list[-1]=field_list[-1].strip('&#xd;\n')
value_list_1d = []
for l in lines[1:]:
    value_list_1d.append(l)
value_list=[]
for entry in value_list_1d:
    indexed_list = parse_string(entry)
    value_list.append(indexed_list)


'''---------------------------------
Convert lists into dictionary
use dictionary to create Json
---------------------------------'''
#format value list manually to fit json requirements
json_formater(value_list)
#create dictionary with field and values 
json_dict=dictionify(value_list,field_list)
# dev_print_dict_n(json_dict)
print(json.dumps(json_dict))