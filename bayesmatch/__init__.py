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


def member_df_to_names(member_df):
    for column_name in ["first_name", "last_name", "nickname"]:
        column = member_df[column_name]
        for value in column:
            if pd.notna(value):
                for name in ProcessName(value):
                    yield name


default_rare = 1e-5

#!!!cmk move ipython for name to prob to this project, too.


def prob_of_each_member_name():
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

    member_name_to_probability = {
        (name, name_to_probability.get(name, default_rare))
        for name in member_df_to_names(member_df)
    }
    member_name_to_probability = sorted(member_name_to_probability, key=lambda x: x[1])
    print(member_name_to_probability[:5])
    # [('POCAN', 3e-07), ('GROTHMAN', 4e-07), ('GOSAR', 4e-07), ('MOOLENAAR', 4e-07), ('MASTO', 4e-07)]
    print(member_name_to_probability[-5:])
    # [('MARY', 0.02629), ('MICHAEL', 0.02629), ('ROBERT', 0.03143), ('JOHN', 0.0327099999999999), ('JAMES', 0.03318)]


if __name__ == "__main__":
    prob_of_each_member_name()
