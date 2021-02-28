import os

import pandas as pd

scheduler_list = os.listdir("./experiments/")
scheduler_list.remove(".gitkeep")

results_df = pd.DataFrame(columns=["scheduler", "path_1_bw", "path_2_bw", "latency", "transfer_time"])
sch_col, path_1_col, path_2_col, latency_col, tr_col = [], [], [], [], []
for scheduler in scheduler_list:
    samples = os.listdir(f'./experiments/{scheduler}/')
    for case in samples:
        avg_transfer_time = 0
        for i in range(0, 10):
            file = open(f'./experiments/{scheduler}/{case}/client_{i}.txt', "r")
            content = file.readlines()
            transfer_time = content[2].split(":")[2].strip().split(" ")[0]
            avg_transfer_time += float(transfer_time)
        avg_transfer_time /= 10
        details = case.split("_")
        sch_col.append(scheduler)
        path_1_col.append(details[0])
        path_2_col.append(details[1])
        latency_col.append(details[2][:len(details[2]) - 2] if "ms" in details[2] else details[2])
        tr_col.append(avg_transfer_time)

results_df['scheduler'], results_df['path_1_bw'], results_df['path_2_bw'] = sch_col, path_1_col, path_2_col
results_df['latency'], results_df['transfer_time'] = latency_col, tr_col
results_df.to_csv("./results.csv")
