# ProbeFinder
Retrieves the chromosome, position and strand of given probes in the EPIC methylation arrays probe database and subsequently converts positions to hg38.

## QuickGuide
1- Download the program
	git clone https://github.com/superDross/ProbeFinder

2 - Ensure to copy the epic-array probes over
	cp dmp-epic_values_AllProbes.csv probeFinder/

3 - Create an input file that has a column of probe names and save it as a tab-delimited csv e.g. file name InProbes.txt 
with the following column:
	cg00017461
	cg07481320
	cg12435154
	...

4 - Execute the command
	cd ProbeFinder/
	python3 -i InProbes.txt -d dmp-epic_values_AllProbes.csv -o OutProbes.txt

5 - Print the output file 
	cat OutProbes.txt

OutProbes.txt can be used as input for the ```--cpg``` option in [MethyCoverageParser](https://github.com/superDross/MethyCoverageParser)
