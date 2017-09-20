import re
import os
import sys
import subprocess
import argparse
import site_conversion as sc

# path to his dir
HERE = os.path.dirname(os.path.realpath(__file__))

def main(probe_file, out_file, database):
    ''' Get genomic positions of all probes, convert to positive strand
        and convert to hg38 positions.

    Args:
        probe_file: file containing a probe ID on each line (txt file with column of probe names)
        out_file: name of output
        database: file containing all probe info (genomic pos, strand etc.)

    '''
    # default database
    database = HERE+"/dmp-epic_values_AllProbes.csv" if not database else database
    
    # get positions of probes and output to probe_hg19.tsv
    print("\n{}\nSearching {} for probes within {}\n{}\n".format("#"*75, database.split("/")[-1],probe_file, "#"*75))
    get_probe_info(probe_file, database)

    # convert to liftover input format and convert all - to = starnd positions
    sc.strand_convert("probe_hg19.tsv", 'lift_in.pos')

    # convert to hg38 positions
    print("Converting to hg38....")
    hg38_conversion()

    # reconfigure to a tab delimited output and cleanup processing files
    sc.reconfigure_output('converted.txt', out_file)
    sc.clean_up()
    os.remove("probe_hg19.tsv")
    print("Finished!")


def get_probe_info(probe_file, database):
    ''' Get the chromosome, position and strand information
        from a database for each probe in probe_file.
    '''
    with open("probe_hg19.tsv", 'w') as out:
        out.write("Probe\tChromosome\tPosition\tStrand\n")
        for probe in open(probe_file):
            probe = probe.rstrip()
            info = None # needed for error catching
            # check each line of the database for the probe
            for line in open(database):
                line = line.rstrip()
                if re.search(probe, line):
                    sline = line.split(",")
                    # probe   chrom   pos   strand
                    info = "\t".join([sline[1], sline[7], sline[8], sline[9]])
                    info = info.replace("\"", '')
                    out.write(info+"\n")            

            # catch probes not found
            if not info:
                print("{} was not found within {}".format(probe, database.split("/")[-1]))


def hg38_conversion():
    ''' Convert probe positions to hg38.
    '''
    if sys.platform == "linux" or sys.platform == "linux2":
        print("Detected linux OS....")
        subprocess.call([HERE+'/LiftOver/liftOver', '-positions', 'lift_in.pos', 
                         HERE+"/LiftOver/hg19ToHg38.over.chain", 'converted.txt', 'unMapped'])
    elif sys.platform == "darwin":
        print("Detected Mac OS....")
        subprocess.call([HERE+'/LiftOver/liftOver_mac', '-positions', 'lift_in.pos', 
                         HERE+"/LiftOver/hg19ToHg38.over.chain", 'converted.txt', 'unMapped'])
    else:
        print(str(sys.platform)+" OS {} is unsupported. Exiting.".format(sys.platform))
        sys.exit()


def cli():
    parser = argparse.ArgumentParser(description="extract genomic positions of probes from a database, convert strand to positive and convert to hg38 positions.")
    parser.add_argument('-i', '--probes', help='file containing probe ids')
    parser.add_argument('-d', '--database', action='store_true', help='file containing all probe info (genomic position etc.')
    parser.add_argument('-o', '--out', help='name of output file')

    args = vars(parser.parse_args())
    main(args['probes'], args['out'], args['database'])


if __name__ == "__main__":
    cli()
