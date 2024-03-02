import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from cycler import cycler

# colors = cycler(color=plt.get_cmap("tab10").colors)  # ["b", "r", "g"]
# colors = cycler(color=["#282782", "r", "g"])

mpl.style.use("ggplot")
mpl.rcParams["figure.figsize"] = (16 / 2.54, 9 / 2.54)
mpl.rcParams["axes.facecolor"] = "white"
mpl.rcParams["axes.grid"] = True
mpl.rcParams["grid.color"] = "lightgray"
# mpl.rcParams["axes.prop_cycle"] = colors
mpl.rcParams["axes.linewidth"] = 1
mpl.rcParams["xtick.color"] = "black"
mpl.rcParams["ytick.color"] = "black"
mpl.rcParams["font.size"] = 12
mpl.rcParams["figure.titlesize"] = 25
mpl.rcParams["figure.dpi"] = 100

sns.set_style("white")
sns.set_context("notebook")
sns.set_palette("colorblind")
