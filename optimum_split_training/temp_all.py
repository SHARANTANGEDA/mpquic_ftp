import pandas as pd

df = pd.read_csv("intermediate_results_my_machine.csv")

grp = df.groupby(["path_1_bw", "delay_1", "loss_1", "path_2_bw", "delay_2", "loss_2"])

plot = []

cnt = 0
for idx, items in grp:
    for row_index, row in items.iterrows():
        plot.append((cnt, idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], row["split_ratio"], row["transfer_time"]))
    cnt += 1

df_plot = pd.DataFrame(data=plot,
                       columns=["Id", "path_1_bw", "delay_1", "loss_1", "path_2_bw", "delay_2", "loss_2", "split_ratio",
                                "transfer_time"])

df_plot.to_csv("inter_res_my.csv", index=False)
