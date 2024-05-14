import json
import argparse
import os

parser = argparse.ArgumentParser(description='Output proper notebook.')
parser.add_argument('-i', '--input', type=str, help='notebook to be processed.')
parser.add_argument('-o', '--output', type=str, required=False, help='output name of notebook.')

args = parser.parse_args()

if '.ipynb' not in args.input: args.input += '.ipynb'
if args.output:
    if '.ipynb' not in args.output:
        args.output += '.ipynb'

with open(args.input, 'r') as file:
    data = file.read()

data_j: str = json.loads(data)

for cell in data_j['cells']:
    if cell['cell_type'] == 'markdown':
        cell['source'] = list(map(str.strip, cell['source']))

    if cell['cell_type'] == 'code':
        if '# %%' in cell['source'][0]:
            cell['source'] = cell['source'][1:]

        for idx in range(len(cell['source'])):
            if cell['source'][idx] != '\n':
                cell['source'] = cell['source'][idx:]
                break

        for idx in reversed(range(len(cell['source']))):
            if cell['source'][idx] != '\n':
                cell['source'] = cell['source'][:idx+1]
                break

    cell['source'][-1] = cell['source'][-1].rstrip()


if not args.output:
    notebook_files = [file for file in os.listdir() if '.ipynb' in file]
    assert len(notebook_files) == 2, 'You can omit a destination notebook for the output if there are exactly two notebooks in the directory. In other cases please specify a destination notebook with the -o flag.'
    for file in notebook_files:
        if file != args.input:
            destination_notebook = file
    with open(destination_notebook, 'w') as result:
        result.write(json.dumps(data_j))
else:
    with open(args.output, 'w') as result:
        result.write(json.dumps(data_j))

print('[+] Finished clean up process for notebook.')


