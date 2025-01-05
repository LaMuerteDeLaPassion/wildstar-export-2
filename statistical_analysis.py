from m3reader import *
import os

path = os.getcwd()+"\\m3"

with open('statistical_analysis.csv', 'w') as f:
    header = Header()
    fields = ""
    for field, value in vars(header).items():
        fields += field + ","
    f.write(fields)
    f.write('\n')
    for filename in os.listdir(path):
        values = ""
        with open(os.path.join(path, filename), 'rb') as br: # open in readonly mode
            header = Header.read_header(br, only_header=True, name=filename)
        for field, value in vars(header).items():
            values += str(value) + ","
        f.write(values)
        f.write('\n')