import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set(style="white")

results_df = pd.read_csv("./results.csv")

for region, df_plot in results_df.groupby(["path_1_bw", "path_2_bw", 'latency']):
    plot = sns.barplot(df_plot['scheduler'], df_plot['avg_transfer_time']).set_title(
        f'Bandwidth: Path-1: {region[0]}Mbps, Path-2: {region[1]}Mbps, Latency: {region[2]}ms', fontsize=18)
    # plot.set_xlabels('Scheduler', fontsize=12)
    # plot.set_ylabels('Avg Transfer Time(Avg. of 10 runs)', fontsize=12)
    plt.xticks(plt.xticks()[0], rotation=35)
    plt.tight_layout()
    figure = plot.get_figure()
    figure.savefig(f'./plots/{region[0]}_{region[1]}_{region[2]}.png', dpi=600, bbox_inches="tight")
    figure.clear()
    plt.close(figure)
