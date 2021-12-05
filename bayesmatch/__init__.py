import pandas as pd

# import numpy as np

if __name__ == "__main__":
    # Find the probability of each first name, last name, and nickname in the club.

    # !!!cmk pull example from from the internet
    member_file = r"D:\OneDrive\Shares\RaceResults\sample_members.tsv"

    member_df = pd.read_csv(member_file, sep="\t")
    print(member_df)
