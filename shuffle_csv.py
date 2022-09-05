import pandas
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit(1)
    infile = sys.argv[1]
    outfile = sys.argv[2]
    df = pandas.read_csv(infile)
    shuffled_df = df.sample(frac=1)
    shuffled_df.to_csv(outfile, index=False)
