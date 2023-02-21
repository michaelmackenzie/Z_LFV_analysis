import json
import glob
import argparse

#-----------------------------------------------------------
def check_overlap(current, new):
    # for each added lumi range, check if it exists in the current list
    for added in new:
        if len(added) < 2: continue
        for pair in current:
            if len(pair) < 2: continue
            lumi = added[0]
            if lumi >= pair[0] and lumi <= pair[1]:
                return True
            lumi = added[1]
            if lumi >= pair[0] and lumi <= pair[1]:
                return True
    return False

#-----------------------------------------------------------
def merge_run(current, new):
    current.sort()
    new.sort()
    runs = current + new
    runs.sort()
    if len(runs) < 2: return runs, False
    merged = []
    #for each run, see if it can join with a neighbor
    run = runs[0]
    applied_merge = False
    for index in range(len(runs)-1):
        if run[1] >= runs[index+1][0]-1: #if it can be merged, merge it and continue
            run = [run[0], max(run[1], runs[index+1][1])]
            applied_merge = True
        else: #if it can't be merged, store the run and move onto the next one
            merged.append(run)
            run = runs[index+1]
            index += 1 #skip the next run as it has already been checked
    # if applied_merge:
    #     print current
    #     print new
    #     print merged
    merged.append(run)
    return merged, applied_merge
    

#-----------------------------------------------------------
p = argparse.ArgumentParser(description='Merge input lumi json files into a single json file')
p.add_argument('input_tag'  , help='Input file path')
p.add_argument('--out_name' , help='Output file path', default="file_lumis_merged_JSON.txt", required=False)
p.add_argument('--verbose'  , help='Increase output information', action='store_true', required=False)
p.add_argument('--overlap'  , help='Warn on overlap between lumi files', action='store_true', required=False)
p.add_argument('--throw_on_overlap'  , help='Throw on overlap between lumi files', action='store_true', required=False)
p.add_argument('--onlycheck', help='Process without writing a new json file', action='store_true', required=False)

args = p.parse_args()
input_tag = args.input_tag
out_name = args.out_name
verbose = args.verbose
throw_on_overlap = args.throw_on_overlap
overlap = throw_on_overlap or args.overlap
onlycheck = args.onlycheck

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
for index, json_file in enumerate(json_list):
    if verbose: print "Merging file %s" % file_list[index]
    for run in json_file:
        run_val = str(run)
        if run_val in all_runs.keys():
            if overlap and check_overlap(all_runs[run_val], json_file[run]):
                print "Overlap for json file %s (run %s)" % (file_list[index], run_val)
                if throw_on_overlap: exit()
            # all_runs[run_val] += json_file[run]
            new_runs, merged = merge_run(all_runs[run_val], json_file[run])
            # if merged: exit()
            all_runs[run_val] = new_runs
        else:
            all_runs[run_val] = json_file[run]


if onlycheck:
    exit()

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
