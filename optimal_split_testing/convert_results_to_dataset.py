import os

import pandas as pd

import utils

results_df = pd.DataFrame(columns=["path_1_bw", "delay_1", "loss_1", "path_2_bw", "delay_2", "loss_2", "split_ratio",
                                   "transfer_time"])
path_1_col, delay_1_col, loss_1_col, path_2_col, delay_2_col, loss_2_col, split_ratios_list, tr_col = [], [], [], [], \
                                                                                                      [], [], [], []
scheduler_col = []
_, _, _, _, runs_per_combination = utils.load_config()

samples = os.listdir(f'./results/')
samples.remove(".gitkeep")
# samples.remove(".DS_Store")
for idx, case in enumerate(samples):
    for i in range(0, runs_per_combination):
        transfer_time, avail_cnt, excep_cnt = 0, 0, 0
        file = open(f'./results/{case}/server_{i}.txt', "r")
        content = file.readlines()
        # print(content)
        try:
            transfer_time = content[8].split(":")[1].strip().split(" ")[0]
        except:
            print(content, case)

        details = case.split("_")
        path_1_col.append(details[0])
        delay_1_col.append(details[1][:len(details[1]) - 2] if "ms" in details[1] else details[1])
        loss_1_col.append(details[2])
        path_2_col.append(details[3])
        delay_2_col.append(details[4][:len(details[4]) - 2] if "ms" in details[4] else details[4])
        loss_2_col.append(details[5])
        try:
            split_ratios_list.append(content[4].split(":")[2].strip())
        except:
            split_ratios_list.append(content[4].split(":")[1].strip())
        tr_col.append(transfer_time)
        scheduler_col.append(details[6])



results_df['path_1_bw'], results_df['delay_1'], results_df['loss_1'], results_df['path_2_bw'], results_df['delay_2'], \
results_df['loss_2'] = path_1_col, delay_1_col, loss_1_col, path_2_col, delay_2_col, loss_2_col
results_df['split_ratio'], results_df['transfer_time'], results_df['scheduler'] = split_ratios_list, tr_col, \
                                                                                  scheduler_col
results_df.to_csv("./test_paper_v2.csv", index=False)
