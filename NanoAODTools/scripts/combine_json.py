import json
import glob
import argparse

p = argparse.ArgumentParser(description='Merge input lumi json files into a single json file')
p.add_argument('input_tag'  , help='Type e.g. input file path')
p.add_argument('--out_name'   , help='Type e.g. output file path', default="", required=False)

args = p.parse_args()
input_tag = args.input_tag
out_name = args.out_name
if out_name == "":
    out_name = "file_lumis_merged_JSON.txt"

file_list = glob.glob("%s*.txt" % (input_tag))

json_list = []

for file in file_list:
    with open(file, "rb") as f:
        json_list.append(json.load(f))

all_runs = {}
for json_file in json_list:
    for run in json_file:
        run_val = str(run)
        if run_val in all_runs.keys():
            all_runs[run_val] += json_file[run]
        else:
            all_runs[run_val] = json_file[run]

file_merged = open(out_name, 'w')
# file_merged.write(str(all_runs))

file_merged.write('{\n')
runs = all_runs.keys()
runs.sort()
for index,run in enumerate(runs):
    if index < len(all_runs) - 1:
        file_merged.write("  \"%s\": %s,\n" % (run, all_runs[run]))
    else:
        file_merged.write("  \"%s\": %s\n" % (run, all_runs[run]))
file_merged.write('}')
file_merged.close()
