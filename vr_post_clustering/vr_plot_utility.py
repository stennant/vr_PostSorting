import matplotlib.pylab as plt


def draw_reward_zone():
    for stripe in range(8):
        if stripe % 2 == 0:
            plt.axvline(91.25+stripe*2.5, color='limegreen', linewidth=5.5, alpha=0.4, zorder=0)
        else:
            plt.axvline(91.25+stripe*2.5, color='k', linewidth=5.5, alpha=0.4, zorder=0)


def draw_black_boxes():
    plt.axvline(15, color='k', linewidth=66, alpha=0.25, zorder=0)
    plt.axvline(185, color='k', linewidth=66, alpha=0.25, zorder=0)


def adjust_spines(ax,spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward',0)) # outward by 10 points
            #spine.set_smart_bounds(True)
        else:
            spine.set_color('none') # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])




def adjust_spine_thickness(ax):
    for axis in ['left','bottom']:
        ax.spines[axis].set_linewidth(2)



def makelegend(fig,ax, x):
    handles, labels = ax.get_legend_handles_labels()
    leg = fig.legend(handles,labels, loc="upper right", bbox_to_anchor=(0.989, x), fontsize = "xx-large")
    for l in leg.get_lines():l.set_linewidth(2)
    frame  = leg.get_frame()
    frame.set_edgecolor('w')
    frame.set_alpha(0.2)


def plot_basics(prm,ax):
        ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis

