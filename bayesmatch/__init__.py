import pandas as pd
import numpy as np
import re

####################################
# Currently the notebook "bayesmatch.ipynb" is
# the best version of this code.
# For now, ignore this file.
####################################


# import numpy as np


def process_name(field):
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


def member_df_to_first_last(member_df):
    for row in member_df.itertuples():
        first_name = ProcessName(row.first_name)
        if len(first_name) > 0:
            first_name = first_name[0]
        else:
            first_name = None
        last_name = ProcessName(row.last_name)
        if len(last_name) > 0:
            last_name = last_name[0]
        else:
            last_name = None
        yield first_name, last_name


default_rare = 1e-5


def load_name_to_prob():
    name_probability_file = r"D:\OneDrive\Shares\RaceResults\name_probability.tsv"
    name_to_probability_df = pd.read_csv(name_probability_file, sep="\t")
    name_to_probability_df.set_index("name", inplace=True)
    name_to_probability = name_to_probability_df.to_dict()["probability"]
    return name_to_probability


# !!!cmk move ipython for name to prob to this project, too.


def prob_of_each_member_name():
    # Find the probability of each first name, last name, and nickname in the club.

    # !!!cmk pull example from from the internet
    member_file = r"D:\OneDrive\Shares\RaceResults\sample_members.tsv"
    member_df = pd.read_csv(member_file, sep="\t")
    # print(member_df)

    name_to_prob = load_name_to_prob()

    member_name_to_probability = {
        (name, name_to_prob.get(name, default_rare))
        for name in member_df_to_names(member_df)
    }
    member_name_to_probability = sorted(member_name_to_probability, key=lambda x: x[1])
    print(member_name_to_probability[:5])
    # [('POCAN', 3e-07), ('GROTHMAN', 4e-07), ('GOSAR', 4e-07), ('MOOLENAAR', 4e-07), ('MASTO', 4e-07)]
    print(member_name_to_probability[-5:])
    # [('MARY', 0.02629), ('MICHAEL', 0.02629), ('ROBERT', 0.03143), ('JOHN', 0.0327099999999999), ('JAMES', 0.03318)]


def prob_of_each_member_full_name():
    # Find the probability of each first name, last name, and nickname in the club.

    # !!!cmk pull example from from the internet
    member_file = r"D:\OneDrive\Shares\RaceResults\sample_members.tsv"
    member_df = pd.read_csv(member_file, sep="\t")
    # print(member_df)

    name_to_prob = load_name_to_prob()

    member_name_to_probability = {
        (
            f"{first} {last}",
            name_to_prob.get(first, default_rare)
            * name_to_prob.get(last, default_rare),
        )
        for first, last in member_df_to_first_last(member_df)
    }
    member_name_to_probability = sorted(member_name_to_probability, key=lambda x: x[1])
    print(member_name_to_probability[:5])
    # [('CHELLIE PINGREE', 3.3784536365974863e-12), ('AUMUA RADEWAGEN', 6e-12), ('None STEUBE', 7.000000000000002e-12), ('KAIALII KAHELE', 1.2e-11), ('KWEISI MFUME', 2.516930241173405e-11)]
    print(member_name_to_probability[-5:])
    # [('MARY MILLER', 0.0001114696), ('JOHN JOYCE', 0.00011906439999999963), ('DAVID SCOTT', 0.00012901979999999945), ('JOHN CARTER', 0.00016170244386560871), ('ROBERT SCOTT', 0.00017160779999999997)]


def odds(prob):
    return prob / (1.0 - prob)


def log_odds(prob):
    return np.log(odds(prob))


def prob(log_odds):
    odds = np.exp(log_odds)
    prob = odds / (odds + 1.0)
    return prob


def prior():
    prob_member_in_race = 0.01
    line_count = 1000

    prob_line_is_about_member = prob_member_in_race / line_count

    odds_line_is_about_member = odds(prob_line_is_about_member)
    log_odds_line_is_about_member = log_odds(prob_line_is_about_member)
    print(
        f"prob={prob_line_is_about_member}, odds={odds_line_is_about_member:.10f}, log_odds={log_odds_line_is_about_member:.2f}"
    )

    return log_odds_line_is_about_member


def coincidental(name):
    print(len(load_name_to_prob()))

    name_to_prob = load_name_to_prob()
    print(name_to_prob["ROBERT"])
    print(name_to_prob["PINGREE"])

    return name_to_prob[name]


prob_name_in_result = 0.6


if __name__ == "__main__":
    # prob_of_each_member_name()
    # prior()
    # prob_of_each_member_full_name()
    # coincidental()

    log_odds_prior = prior()
    print(f"log_odds_prior={log_odds_prior}")

    prob_name_in_result = 0.6
    prob_coincidental = coincidental("ROBERT")
    log_bayes_factor = np.log(prob_name_in_result / prob_coincidental)
    print(f"log_bayes_factor={log_bayes_factor}")

    log_odds_posterior = log_odds_prior + log_bayes_factor
    print(f"log_odds_posterior={log_odds_posterior}")
    print(f"posterior={prob(log_odds_posterior)}")
