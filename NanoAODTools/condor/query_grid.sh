#! /bin/bash

SUMMARY=""
if [[ "$1" == "s" ]]
then
  SUMMARY="s"
fi

date
condor_q | awk -v user=${USER} -v summary=${SUMMARY} '
{
    if($2 == user) {
        ++total
        split($1,arr,".")
        name=arr[1]
        users[name] = $2
        if(name in names) {
            ++names[name]
        } else {
            names[name] = 1;
            status[name]["I"] = 0;
            status[name]["R"] = 0;
            status[name]["H"] = 0;
            status[name]["X"] = 0;
	    scripts[name] = $9;
	    for(i = 10; i < NF; ++i) {
		if($i ~ /_/) {
		    datasets[name] = $i;
		    i = NF + 1;
		}
	    }
        }
        ++statuses[name][$6]
	++counts[$9];
	++script_statuses[$9][$6];
	# } else if($2 == "jobs;") {
    #     print "JobSub grid summary:",$0
    }
} END {
    print "Jobsub summary: Total of",total,"jobs found for user",user
    if(summary != "s") {
	print "User       Job-ID              Total      Idle   Running      Held         X               dataset                                     script"
	for(name in names) {
	    printf "%-10s %-10s %14i %9i %9i %9i %9i   %-50s %s\n", users[name], name, names[name],
		statuses[name]["I"], statuses[name]["R"], statuses[name]["H"], statuses[name]["X"], datasets[name], scripts[name];
	}
    }
    print "Job script               :     Total      Idle   Running      Held         X"
    for(script in counts) {
	printf "%-25s: %9i %9i %9i %9i %9i\n", script, counts[script], script_statuses[script]["I"], script_statuses[script]["R"],
	    script_statuses[script]["H"], script_statuses[script]["X"];
    }
 }'

# This tells emacs to view this file in awk mode.
# Local Variables:
# mode: awk
# End:
