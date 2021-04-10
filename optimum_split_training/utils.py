import itertools
import json

import pandas as pd


def load_config():
    file = open("config.json", "r")
    config = json.load(file)
    return config["path_1"], config["path_2"], config["maximum_experiment_count"], config["split_ratios"], config[
        "runs_per_combination"]


def generate_all_combinations(bw_1_list, delay_1_list, loss_1_list, bw_2_list, delay_2_list, loss_2_list):
    perms = list(itertools.product(*[bw_1_list, delay_1_list, loss_1_list, bw_2_list, delay_2_list, loss_2_list]))
    print(len(perms))
    return perms


def save_combinations_as_df(combinations, file_name="combinations.csv"):
    df = pd.DataFrame(data=combinations,
                      columns=["path_1_bw", "path_1_delay", "path_1_loss", "path_2_bw", "path_2_delay",
                               "path_2_loss"])
    df.to_csv(file_name, index=False)
    return df
