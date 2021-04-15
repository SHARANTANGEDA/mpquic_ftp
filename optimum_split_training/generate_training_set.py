import pandas as pd

df = pd.read_csv("./intermediate_results.csv")

grouped_results = df.groupby(["path_1_bw", "delay_1", "loss_1", "path_2_bw", "delay_2", "loss_2"])

path_1_col, delay_1_col, loss_1_col, path_2_col, delay_2_col, loss_2_col, split_ratios_list = [], [], [], [], [], [], []
for group_name, df_group in grouped_results:
    best_split, best_transfer_time = -1, -1
    for row_index, row in df_group.iterrows():
        tr, split = row['transfer_time'], row['split_ratio']
        if best_transfer_time == -1:
            best_split = split
            best_transfer_time = tr
        elif best_transfer_time > tr:
            best_split = split
            best_transfer_time = tr
    path_1_col.append(group_name[0])
    delay_1_col.append(group_name[1])
    loss_1_col.append(group_name[2])
    path_2_col.append(group_name[3])
    delay_2_col.append(group_name[4])
    loss_2_col.append(group_name[5])
    split_ratios_list.append(best_split)

results_df = pd.DataFrame(columns=["path_1_bw", "delay_1", "loss_1", "path_2_bw", "delay_2", "loss_2", "split_ratio"])

results_df['path_1_bw'], results_df['delay_1'], results_df['loss_1'], results_df['path_2_bw'], results_df['delay_2'], \
results_df['loss_2'] = path_1_col, delay_1_col, loss_1_col, path_2_col, delay_2_col, loss_2_col
results_df['split_ratio'] = split_ratios_list

results_df.to_csv("./results_dataset.csv", index=False)

