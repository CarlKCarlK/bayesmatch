import pandas as pd
import re

# import numpy as np


def ProcessName(field):
    # Rules for names:
    #     Assume no accent marks !!!TODO
    #     trim spaces from ends !!!TODO
    #     capitalize everything
    #     make any middle name part of the first or last name via spaces
    #     Remove "." and "'"
    #     ignore any one character names
    #     Split on hyphens, slashes, and spaces and treat as nicknames
    #     treat the nickname column as a first name nickname
    #     remove empty strings

    field = field.upper().strip()

    # TODO what about other single-quote like characters such as back quote
    field = field.replace(".", "").replace("'", "")

    # TODO about about spliting on all whitespace?
    names = re.split(r"-|/|\s+", field)
    names2 = [name for name in names if len(name) > 1]
    return names2


default_rare = 1e-5

if __name__ == "__main__":
    # Find the probability of each first name, last name, and nickname in the club.

    # !!!cmk pull example from from the internet
    name_probability_file = r"D:\OneDrive\Shares\RaceResults\name_probability.tsv"
    member_file = r"D:\OneDrive\Shares\RaceResults\sample_members.tsv"

    name_to_probability_df = pd.read_csv(name_probability_file, sep="\t")
    name_to_probability_df.set_index("name", inplace=True)
    name_to_probability = name_to_probability_df.to_dict()["probability"]
    # print(name_to_probability)

    member_df = pd.read_csv(member_file, sep="\t")
    # print(member_df)

    for column_name in ["first_name", "last_name", "nickname"]:
        column = member_df[column_name]
        for value in column:
            if pd.notna(value):
                for name in ProcessName(value):
                    prob = name_to_probability.get(name, default_rare)
                    print(f"{name} {prob}")
