import json
import glob
import argparse

p = argparse.ArgumentParser(description='Merge input lumi json files into a single json file')
p.add_argument('input_tag'  , help='Input file path')
p.add_argument('--out_name' , help='Output file path', default="file_lumis_merged_JSON.txt", required=False)
p.add_argument('--verbose'  , help='Increase output information', action='store_true', required=False)

args = p.parse_args()
input_tag = args.input_tag
out_name = args.out_name
verbose = args.verbose

file_list = glob.glob("%s*.txt" % (input_tag))

if len(file_list) == 0:
    print "No files found matching input tag", input_tag
    exit()

json_list = []

for file in file_list:
    if verbose: print "Opening file %s" % (file)
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
print "Writing to file", out_name

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
