import json
import argparse

# TODO: output to only other existing notebook besides the input one
parser = argparse.ArgumentParser(description='Output proper notebook.')
parser.add_argument('-i', '--input', type=str, help='notebook to be processed.')
parser.add_argument('-o', '--output', type=str, help='output name of notebook.')

args = parser.parse_args()

if '.ipynb' not in args.input: args.input += '.ipynb'
if '.ipynb' not in args.output: args.output += '.ipynb'

with open(args.input, 'r') as file:
    data = file.read()

data_j: str = json.loads(data)

for cell in data_j['cells']:
    if cell['cell_type'] == 'markdown':
        cell['source'] = list(map(str.strip, cell['source']))

    if cell['cell_type'] == 'code':
        if '# %%' in cell['source'][0]:
            cell['source'] = cell['source'][1:]
        code_length = len(cell['source'])
        for idx, line in enumerate(cell['source']):
            if idx > code_length - 10 and line == '\n':
                cell['source'].remove(line)
        cell['source'][-1] = cell['source'][-1].strip()


with open(args.output, 'w') as result:
    result.write(json.dumps(data_j))


