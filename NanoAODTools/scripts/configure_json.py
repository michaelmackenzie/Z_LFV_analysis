import json
import argparse

def check_lumi(lumi, lumis):
    for section in lumis:
        if lumi >= section[0] and lumi <= section[1]:
            return True
    return False

def parse_lumi_list(run, lumis, mask):
    lumi_list = []
    curr_lumi = []
    if mask != None:
        if run in mask.keys():
            mask_lumis = mask[run]
        else:
            return []
    prev_lumi = -99
    for lumi in lumis:
        if mask is not None and not check_lumi(lumi, mask_lumis):
            continue;
        if curr_lumi == []: #first loop
            curr_lumi.append(lumi)
        elif prev_lumi != lumi - 1: #add the range of lumis
            curr_lumi.append(prev_lumi)
            lumi_list.append(curr_lumi)
            curr_lumi = [lumi]
        prev_lumi = lumi
    if prev_lumi > -1:
        curr_lumi.append(prev_lumi)
        lumi_list.append(curr_lumi)
    return lumi_list

p = argparse.ArgumentParser(description='Reformat dasgoclient json into brilcalc format')
p.add_argument('--input'  , help='Input file name')
p.add_argument('--output' , help='Output file name')
p.add_argument('--mask' , help='JSON file for lumi masking', default="", required=False)

args = p.parse_args()
input_name = args.input
output_name = args.output
mask_name = args.mask
mask = None

with open(input_name, "rb") as f:
    input_json = json.load(f)
if mask_name != "":
    with open(mask_name, "rb") as f:
        mask = json.load(f)
data = input_json["data"]

runs = {}

for record in data:
    run_number = record["run"][0]["run_number"]
    lumis = record["lumi"][0]["number"]
    lumis.sort()
    lumis = parse_lumi_list(str(run_number), lumis, mask)
    if lumis != []:
        runs[run_number] = lumis

file_merged = open(output_name, 'w')
file_merged.write('{\n')

run_list = runs.keys()
run_list.sort()
for index,run in enumerate(run_list):
    if index < len(runs) - 1:
        file_merged.write("  \"%s\": %s,\n" % (run, runs[run]))
    else:
        file_merged.write("  \"%s\": %s\n" % (run, runs[run]))
file_merged.write('}')
file_merged.close()
