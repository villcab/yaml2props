import argparse
import os.path
import pyperclip
import re

parser = argparse.ArgumentParser(
    prog='YAML2Properties',
    description='Simple script for convert YAML to Properties file format.'
)
parser.add_argument('file', help='Path of YAML file')
parser.add_argument('output_dir', help='Path to output props file')

args = parser.parse_args()

print('YAML File: %s' % args.file)
print('Output Dir: %s' % args.output_dir)

if not os.path.isfile(args.file):
    raise ValueError(args.file + ' is not file')

formatted = ''

with open(args.file) as f:
    lines = f.readlines()

prop = []

output = ''

for line in lines:
    ignore = re.search(r'^\s?[#-]', line)

    if ignore or not line.strip() or not ':' in line:
        output += '\n'
        continue

    tabs = re.findall(r'(\s\s)', line.split(':')[0])

    index = len(tabs) if tabs else 0

    result_prop = re.search(r'.+(?=:\s)', line)
    
    if index == 0:
        prop = []
        prop.append('--' + result_prop.group().strip())
    else:
        prop_name = result_prop.group(0).strip()

        while prop and index < len(prop):
            prop.pop()

        prop.append(prop_name)

    value = re.search(r'(?<=:).+', line)

    if value and value.group().strip():
        p = '.'.join(prop) + "='" + value.group().strip() + "' \\\n"
        output += p

# Prepare write file
splited_name = args.file.split(".")
splited_name2 = splited_name[0].split("/")
fileName = splited_name2[len(splited_name2) - 1]

#file_path = ''.join(splited_name[:len(splited_name) - 1]) + '.properties'
file_path = args.output_dir + fileName + '.properties'

# For debug output
#print(output) 

print('Save to File: ' + file_path)
 
 # Write file
file_props = open(file_path, 'w+')
file_props.write(output)
file_props.close()

print('Done!')