import matplotlib as mpl
import seaborn as sns

def set_plot_style():

    mpl.style.use('ggplot')

    mpl.rcParams.update({
        'axes.facecolor': 'white',
        'axes.linewidth': 1,
        'xtick.color': 'black',
        'ytick.color': 'black',
        'grid.color': 'lightgray',
        'figure.dpi': 100,
        'axes.grid': True,
        'font.size': 12,
    })

    color_palette = [
        '#003851ff', '#3F48F2', '#3F81F2',
        '#3FF2F2', '#9F7FF5', '#90B4F2'
    ]

    sns.set_theme(
        style="whitegrid",
        palette=color_palette,
        font_scale=1.0
    )