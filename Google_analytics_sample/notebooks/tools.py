import matplotlib as mpl
import seaborn as sns

def set_plot_style():

    mpl.style.use('ggplot')

    mpl.rcParams.update({

        'axes.facecolor': 'white',


        'axes.linewidth': 2.0,          
        'axes.edgecolor': 'black',      


        'xtick.color': 'black',
        'ytick.color': 'black',
        'xtick.direction': 'in',        
        'ytick.direction': 'in',
        'xtick.major.size': 6,
        'ytick.major.size': 6,
        'xtick.major.width': 1.5,
        'ytick.major.width': 1.5,


        'grid.color': 'lightgray',
        'axes.grid': False,


        'figure.dpi': 100,


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

    sns.set_style({
        'axes.spines.top': True,
        'axes.spines.right': True,
        'axes.spines.left': True,
        'axes.spines.bottom': True,
    })
