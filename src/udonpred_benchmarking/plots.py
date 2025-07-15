import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotly.express as px
import polars as pl
import seaborn as sns
from matplotlib.gridspec import GridSpec


PALETTE = sns.color_palette("Set1")

grey_ratio = .2
greyed_colors = [PALETTE[0]]
for color in PALETTE[1:]:
    rgb = mcolors.to_rgb(color)
    greyed = [(1- grey_ratio) * c + grey_ratio * .5 for c in rgb]
    greyed_colors.append(greyed)
GREYED_PALETTE = sns.color_palette(greyed_colors)

METHODS = ["UdonPred", "SETH", "PUNCH2", "flDPnn", "AlphaFold2-pLDDT", "AlphaFold3-pLDDT", "ODiNPred"]

FIGURE_KEYWORDS = {
    "figsize": [17 / 2.54, 12 / 2.54],
    "dpi": 300,
    "layout": "compressed"
}

BARPLOT_KEYWORDS = {
    "err_kws": {"linewidth": 1},
    "capsize": .2
}

QUARTILE_BOUNDARIES = [
    0.0821647435897436,
    0.10575444518903224,
    0.1453403565079992,
    0.8710942148760327
]

QUARTILE_LABELS = [
    f"[0, {QUARTILE_BOUNDARIES[0]:.3f})",
    f"[{QUARTILE_BOUNDARIES[0]:.3f}, {QUARTILE_BOUNDARIES[1]:.3f})",
    f"[{QUARTILE_BOUNDARIES[1]:.3f}, {QUARTILE_BOUNDARIES[2]:.3f})",
    f"[{QUARTILE_BOUNDARIES[2]:.3f}, 1]"
]

def label_bars(ax, data, fontsize: int=10, digits: int=3, cutoff: int= 3, **kwargs) -> None:
    for bar in ax.patches[:-cutoff]:
        bar_height = bar.get_height()
        fstring = f"{bar_height:.3f}" if digits == 3 else f"{bar_height:.2f}"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar_height / 2,
            fstring,
            ha="center",
            va="center",
            color="black",
            size=fontsize
        )

def set_theme() -> None:
    sns.set_theme(style="ticks", palette=PALETTE)
