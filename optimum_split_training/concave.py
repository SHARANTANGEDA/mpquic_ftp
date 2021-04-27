import pandas as pd

df = pd.read_csv("inter_res_iters.csv")


plot = []
ratios = [9.0, 4.0, 2.33, 1.5, 1.0, 0.667, 0.4286, 0.25, 0.11, 0]
ratios_map = {
    9.0: "90:10",
    4.0: "80:20",
    2.33: "70:30",
    1.5: "60:40",
    1.0: "50:50",
    0.667: "40:60",
    0.4286: "30:70",
    0.25: "20:80",
    0.11: "10:90",
    0: "0:100"
}

for idx, item in df.iterrows():
    plot.append((item["Id"], item["path_1_bw"], item["delay_1"], item["loss_1"], item["path_2_bw"], item["delay_2"],
                 item["loss_2"], ratios_map[item["split_ratio"]], item["transfer_time"], item["variance"]))

df_plot = pd.DataFrame(data=plot,
                       columns=["Id", "path_1_bw", "delay_1", "loss_1", "path_2_bw", "delay_2", "loss_2", "split_ratio",
                                "transfer_time", "variance"])

df_plot.to_csv("concave_iters.csv", index=False)
