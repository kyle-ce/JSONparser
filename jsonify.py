import json
import re
def dev_print_list_n(field,value):
    #entry number
    n=2
    f_count = 0
    for field_i in field:
        f_count+=1
        print(f_count,". ",field_i)
    v_count=0
    for value_j in value[n]:
        v_count+=1
        print(v_count,". ",value_j)

def dev_print_dict_n(dict):
    for k,v in dict.items():
        print(k,':',v)
    

def jsonify(entry):
    # (?<=...) is a "positive lookbehind assertion". It causes your pattern (in this case, just a comma, ",") to match commas in the string only if they are preceded by the pattern given by .... Here, ... is [\",], which means "either a quotation mark or a comma".
    # (?=...) is a "positive lookahead assertion". It causes your pattern to match commas in the string only if they are followed by the pattern specified as ... (again, [\",]: either a quotation mark or a comma).
    # Since both of these assertions must be satisfied for the pattern to match, it will still work correctly if any of your 'objects' begin or end with commas as well. 
    return re.split(r'(?<=[\",]),(?=[\",])', entry) 

def dictionify(value_list,field_list):
    json_dict={}
    id=0
    for value in value_list:
        id_dict={}
        id+=1
        json_dict[id]=id_dict
        for field in field_list:
            checkIndex(field_list,field,value_list,value)
            id_dict[field]=value[field_list.index(field)]
    return json_dict




def checkIndex(field_list, field_value,value_list, value):
    field_value_index=field_list.index(field_value)
    value_index = value_list.index(value)
    try:
       entry = value_list[value_index][field_value_index]
       value_list[value_index][field_value_index] = entry.strip('&#xd;\n')
    except IndexError:
        value_list[value_index].append('')

#parse response into list 
with open('responseLine.txt')as f:
    lines = f.readlines()

#parse feild values into list
field = lines[0].split(',')
#manualy strip the invalid hex char at end of field value
field[26]=field[26].strip('&#xd;\n')

#parse values into 2D list 
value = []
for l in lines[1:]:
    value.append(l)
#split list into individual values     
value2d=[]
for entry in value:
    json_obj = jsonify(entry)
    value2d.append(json_obj)

json_dict=dictionify(value2d,field)

# dev_print_list_n(field,value2d)

# dev_print_dict_n(json_dict)
print(json.dumps(json_dict))

# combine field with value
# print(len(value2d[0]))
# response = []
# for i in value2d:
#     response.append("},")
#     response.append(i[0]+": {")
#     for j in field[1:]:
#         checkIndex(field,j,value2d,i)
#         obj = j+": "+i[field.index(j)]+","
#         # print(obj)
#         response.append(obj)

# for i in response:
#     print(i)

# checkIndex(field,field[26],value2d,value2d[3])
# print(value2d[3][26])



