import matplotlib.pyplot as plt
import seaborn as sns

def plot_avg_abn(abn_matrix):
    sns.lineplot(data=abn_matrix.mean(axis=1))
    plt.axvline(0, linestyle="--", linewidth=1)
    plt.title("Average abnormal IV around earnings")
    plt.xlabel("Event day (0 = announcement)")
    plt.ylabel("Δ Implied Volatility")
    plt.tight_layout()
    plt.show()

def heatmap_tstats(tstats):
    sns.heatmap(tstats.values.reshape(1,-1), annot=True, fmt=".2f",
                cbar=False, yticklabels=["t-stat"])
    plt.xlabel("Event day")
    plt.title("Panel t-statistics across universe")
    plt.tight_layout()
    plt.show()
