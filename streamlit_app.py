from urllib.error import URLError
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
from matplotlib import cm
import seaborn as sns
import matplotlib.pyplot as plt
import time
import streamlit as st
import numpy as np
import pandas as pd

import os
import glob

import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')


# from scipy.stats import norm, gaussian_kde, percentileofscore

pd.options.display.max_columns = None
# from nba_api.stats.static import players
# from nba_api.stats.endpoints import shotchartdetail
# from nba_api.stats.endpoints import playercareerstats

# For Shot Chart

st.set_page_config(page_title=" Prototype ", page_icon="📈")


sns.set_style('white')
sns.set_color_codes()


def draw_court(ax=None, color="blue", lw=1, shotzone=True, outer_lines=False):
    """Returns an axes with a basketball court drawn onto to it.
    This function draws a court based on the x and y-axis values that the NBA
    stats API provides for the shot chart data.  For example the center of the
    hoop is located at the (0,0) coordinate.  Twenty-two feet from the left of
    the center of the hoop in is represented by the (-220,0) coordinates.
    So one foot equals +/-10 units on the x and y-axis.
    Parameters
    ----------
    ax : Axes, optional
        The Axes object to plot the court onto.
    color : matplotlib color, optional
        The color of the court lines.
    lw : float, optional
        The linewidth the of the court lines.
    outer_lines : boolean, optional
        If `True` it draws the out of bound lines in same style as the rest of
        the court.
    Returns
    -------
    ax : Axes
        The Axes object with the court on it.
    """
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the right side 3pt lines, it's 14ft long before it arcs
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    # Create the right side 3pt lines, it's 14ft long before it arcs
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # Draw shotzone Lines
    # Based on Advanced Zone Mode
    if (shotzone == True):
        shotzone_color = 'gray'
        shotzone_lw = 0.4
        inner_circle = Circle((0, 0), radius=80, linewidth=shotzone_lw,
                              color=shotzone_color, fill=False, linestyle='dashed')
        outer_circle = Circle((0, 0), radius=160, linewidth=shotzone_lw,
                              color=shotzone_color, fill=False, linestyle='dashed')
        corner_three_a_x = Rectangle(
            (-250, 92.5), 30, 0, linewidth=shotzone_lw, color=shotzone_color, linestyle='dashed')
        corner_three_b_x = Rectangle(
            (220, 92.5), 30, 0, linewidth=shotzone_lw, color=shotzone_color, linestyle='dashed')

        # 60 degrees
        inner_line_1 = Rectangle(
            (40, 69.28), 80, 0, 60, linewidth=shotzone_lw, color=shotzone_color, linestyle='dashed')
        # 120 degrees
        inner_line_2 = Rectangle(
            (-40, 69.28), 80, 0, 120, linewidth=shotzone_lw, color=shotzone_color, linestyle='dashed')

        # Assume x distance is also 40 for the endpoint
        inner_line_3 = Rectangle((53.20, 150.89), 290, 0, 70.53,
                                 linewidth=shotzone_lw, color=shotzone_color, linestyle='dashed')
        inner_line_4 = Rectangle((-53.20, 150.89), 290, 0, 109.47,
                                 linewidth=shotzone_lw, color=shotzone_color, linestyle='dashed')

        # Assume y distance is also 92.5 for the endpoint
        inner_line_5 = Rectangle((130.54, 92.5), 80, 0, 35.32,
                                 linewidth=shotzone_lw, color=shotzone_color, linestyle='dashed')
        inner_line_6 = Rectangle((-130.54, 92.5), 80, 0, 144.68,
                                 linewidth=shotzone_lw, color=shotzone_color, linestyle='dashed')

        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc, inner_circle, outer_circle,
                          corner_three_a_x, corner_three_b_x,
                          inner_line_1, inner_line_2, inner_line_3, inner_line_4, inner_line_5, inner_line_6]
    else:
        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    ax.set_xticks([])
    ax.set_yticks([])

    return ax


def shot_chart(data, title="", color="b",
               xlim=(-250, 250), ylim=(422.5, -47.5), line_color="black",
               court_color="white", court_lw=1, outer_lines=False,
               flip_court=False, gridsize=None,
               ax=None, despine=False, **kwargs):

    if ax is None:
        ax = plt.gca()

    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_title(title, fontsize=18)

    # draws the court
    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

    # separate color by make or miss
    # x_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
    # y_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']

    # x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
    # y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']

    # ---------------------------------------------------------------------
    x_missed = data[data['SHOT_MADE_FLAG'] == 0]['LOC_X']
    y_missed = data[data['SHOT_MADE_FLAG'] == 0]['LOC_Y']

    x_made = data[data['SHOT_MADE_FLAG'] == 1]['LOC_X']
    y_made = data[data['SHOT_MADE_FLAG'] == 1]['LOC_Y']
    # ---------------------------------------------------------------------

    # plot missed shots
    ax.scatter(x_missed, y_missed, c='r', marker="x",
               s=300, linewidths=3, **kwargs)
    # plot made shots
    ax.scatter(x_made, y_made, facecolors='none', edgecolors='g',
               marker="o", s=100, linewidths=3, **kwargs)

    # Set the spines to match the rest of court lines, makes outer_lines
    # somewhate unnecessary
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    return ax


st.title('我的第一個應用程式')


@st.cache_data
def get_data():
    FILE_PATH = glob.glob(os.path.join(
        'D:/side_project/tk_test_1023/data/*.csv'))
    colnames = ['GAME_ID', 'PERIOD', 'MINUTES_REMAINING', 'SECONDS_REMAINING',
                'GAME_EVENT_ID', 'TEAM_NAME', 'PLAYER_ID', 'LOC_X', 'LOC_Y', 'SHOT_MADE_FLAG', 'POINTS']
    df_from_each_file = (pd.read_csv(
        f, header=None, delimiter=' ', names=colnames) for f in FILE_PATH)
    df = pd.concat(df_from_each_file, ignore_index=True)
    return df


try:

    df = get_data()
    teams = st.sidebar.multiselect(
        "Choose teams", (list(set(df['TEAM_NAME']))),
    )

    periods = st.sidebar.selectbox(
        "Choose PERIOD", [1, 2, 3, 4], index=None
    )
    if not teams:
        st.error("Please select at least one teams.")
    else:

        with st.form(key='my_form'):
            submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            # Data filter
            df_test = df[df['TEAM_NAME'] == teams[0]]
            print('COUNTS:', df_test.count)
            print('periods', periods, type(periods))
            if periods is not None:
                df_test = df_test[df_test['PERIOD'] == (periods)]
            print('COUNTS:', df_test.count)
            # Show Figure
            demo = df_test
            plt.rcParams['figure.figsize'] = (12, 11)
            shot_chart(demo, title='This is Test')

            st.pyplot(plt.gcf())

except URLError as e:
    st.error(
        """
            **This demo requires internet access.**
            Connection error: %s
        """
        % e.reason
    )
