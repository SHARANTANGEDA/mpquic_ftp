import pandas as pd

import mininet_utils
import utils

# parser = argparse.ArgumentParser(description='Run Automated Testing')
# parser.add_argument('--split_ratio', type=str, dest="split_ratio", help="Split Ratio", default="1.0")
# args = parser.parse_args()
path_1, path_2, max_cnt, split_ratios_list, runs_per_combination = utils.load_config()


df = pd.read_csv("combinations.csv")

# Train and record split ratio for each combination
results, total_cnt, current_cnt = [], len(df), 0
schedulers = ["optimum_split"]
for sch in schedulers:
    for split in split_ratios_list:
        for idx, row in df.iterrows():
            mininet_utils.run_exp_for_combination(row['path_1_bw'], row['delay_1'], row['loss_1'], row['path_2_bw'],
                                                  row['delay_2'], row['loss_2'], sch, split, runs_per_combination)
            current_cnt += 1
            print("Progress: {}/{}; {}% <==> {}/{} {}".format(current_cnt, total_cnt, current_cnt * 100 / total_cnt, idx,
                                                            len(df), sch))
