#!/usr/bin/env python3

# plot a phaseplot of pH and pD for different levels of dispersal

import pandas as pd
import functools
import itertools
import re, string, sys, os
import numpy as np
import subprocess
import matplotlib
matplotlib.use('pgf')
#matplotlib.use('Agg')


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import rcParams
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator
from matplotlib import cm

plt.style.use('base')

rcParams['axes.labelsize'] = 15

pgf_with_custom_preamble = {
    "font.family": "serif", # use serif/main font for text elements
    "text.usetex": True,    # use inline math for ticks
    "pgf.rcfonts": False,   # don't setup fonts from rc parameters
    "pgf.preamble": [
         "\\usepackage{units}",         # load additional packages
         "\\usepackage{metalogo}",
         "\\usepackage{unicode-math}",  # unicode math setup
         r"\setmathfont{MyriadPro-Regular.otf}",
         r"\setmainfont{MyriadPro-Regular.otf}", # serif font via preamble
         ]
}

# add the latex stuff to the rcParams (parameters to plot the things)
matplotlib.rcParams.update(pgf_with_custom_preamble)


ctr = 0

# make stress iterations for this row of the data.frame
def stress_iterations(row):

    # get params
    sNP2P_1 = row["sNP2P_1"]
    sP2NP_1 = row["sP2NP_1"]
    cue_P = row["cue_P"] 
    cue_NP = row["cue_NP"]
    damage_decay = row["damage_decay"]
    hormone_damage = row["hormone_damage"]

    zt_vals = np.random.normal


# the block function
def block(
        gs # gridspec
        ,row
        ,col
        ,data
        ,xlabel=None
        ,ylabel=None
        ,title=None
        ,plot_empty=False
        ,xtick_labels=True
        ,ytick_labels=False
        ,ylim=(-0.05,1.05)
        ,ind_label=True):

    # get the counter for the letter indicator
    global ctr

    # initialize figure
    ax = plt.subplot(gs[row,col])
    
    # number of replicate simulations
    nrepl = data.shape[0]

    for i in nrepl:

        # get data with a 40 timestep iteration
        # x 200 of stress iterations
        stress_iters = stress_iterations(data[i])



    # sort by dispersal
    data = data.sort_values(by=["d"])

    # plot the yvars
    for i, yvar in enumerate(yvars):

        # obtain linestyle
        if yvars_linestyles is None:
            linestyle = "solid"
        else:
            linestyle = yvars_linestyles[i]

        ax.plot(data["d"]
                ,data[yvar] 
                ,label=yvars_labels[i]
                ,color=yvars_colors[i]
                ,linewidth=yvars_lwds[i]
                ,linestyle=linestyle)

    # finalize the plot
    ax = finishblock(
            ax
            ,xlabel
            ,ylabel
            ,title
            ,plot_empty
            ,xtick_labels
            ,ytick_labels
            ,ylim
            ,ind_label)

    return(ax)


def finishblock(
        ax
        ,xlabel=None
        ,ylabel=None
        ,title=None
        ,plot_empty=False
        ,xtick_labels=True
        ,ytick_labels=False
        ,ylim=(-0.05,1.05)
        ,ind_label=True):

    global ctr

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")

    # do axis labeling
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    ax.set_ylim(ylim)
    ax.set_xlim((-0.05,1.05))

    if type(ylabel) == type("string"):
        ax.set_ylabel(ylabel=ylabel)
    
    if type(xlabel) == type("string"):
        ax.set_xlabel(xlabel=xlabel)

    if not xtick_labels:
        ax.xaxis.set_ticklabels([])

    if not ytick_labels:
        ax.yaxis.set_ticklabels([])
   
    if ind_label:
        ax.set_title(loc="left", 
                label=string.ascii_uppercase[ctr], 
                position=(0.0,1.02))

    ctr += 1
    
    if title is not None: 
        ax.set_title(
                label=title, 
                position=(0.5,1.02))


    return(ax)


# read in the data, where helping is conditional
data = pd.read_csv("../../data/summary_stress_autocorr.csv", sep=";")


# initialize the figure
fig = plt.figure(figsize=(5, 5))

# set the graph's grid
# with corresponding widths and heights
widths = [ 1 ]
heights = [ 1 ]

gs = gridspec.GridSpec(
        len(heights), 
        len(widths), 
        width_ratios=widths, 
        height_ratios=heights)

print(data.columns.values)
print(list(data["sP2NP_2"].unique()))
print(list(data["sNP2NP_2"].unique()))


data_subset = data[
        (data["sP2NP_2"] == 0.1)
        & (data["sNP2NP_2"] == 0.1) ]

block(
    gs
    ,row=0
    ,col=0
    ,data = data_subset
    )