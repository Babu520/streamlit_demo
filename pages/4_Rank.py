import streamlit as st

import os
import glob

import pandas as pd
from urllib.error import URLError
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch, Polygon
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(
    page_title="Rank",
    page_icon="🌡️",
)

st.write("#  🔥 Shot Zone Ranking 🔥")
st.markdown(
    """
        ### [目的]     顯示各區域Hot Hand 球員
        ### [計算方式] 
            - #1 投籃數 >= "設定值"
            - #2 比較命中率
            - #3 如果命中率相同，比較 投進數量
        ### [補充] 目前統計至G32
    """
)
def shot_chart(data, title="", color="b",
               xlim=(-250, 250), ylim=(422.5, -47.5), line_color="#D3D3D3",
               court_color="black", court_lw=6, outer_lines=True,
               flip_court=False, gridsize=None,
               ax=None, despine=False, zone_colors=['red'], texts=[''], **kwargs):

    if ax is None:
        ax = plt.gca()
        ax.set_facecolor(court_color)

    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_title(title, pad=20,fontsize=18)

    # draws the court
    draw_court(ax, color=line_color, lw=court_lw,
               outer_lines=outer_lines, zone_colors=zone_colors, texts=texts)

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

def draw_court(ax=None, color="blue", lw=1, shotzone=True, outer_lines=False, zone_colors=['red'], texts=['']):
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
    # hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    # backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    outer_box.set_zorder(10)

    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)
    inner_box.set_zorder(10)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    top_free_throw.set_zorder(10)

    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    bottom_free_throw.set_zorder(10)

    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)
    restricted.set_zorder(10)

    # Three point line
    # Create the right side 3pt lines, it's 14ft long before it arcs
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    # Create the right side 3pt lines, it's 14ft long before it arcs
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)
    three_arc.set_zorder(10)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # Draw shotzone Lines
    # Based on Advanced Zone Mode
    if (shotzone == True):
        shotzone_color = '#D3D3D3'
        # D3D3D3 : gray
        shotzone_lw = 4

        inner_circle = Circle(
            (0, 0), radius=80, linewidth=shotzone_lw, color=shotzone_color, fill=False)

        outer_circle = Circle(
            (0, 0), radius=160, linewidth=shotzone_lw, color=shotzone_color, fill=False)

        corner_three_a_x = Rectangle(
            (-250, 92.5), 30, 0, linewidth=shotzone_lw, color=shotzone_color)
        corner_three_b_x = Rectangle(
            (220, 92.5), 30, 0, linewidth=shotzone_lw, color=shotzone_color)

        # 60 degrees
        inner_line_1 = Rectangle(
            (40, 69.28), 80, 0, 60, linewidth=shotzone_lw, color=shotzone_color)
        # 120 degrees
        inner_line_2 = Rectangle(
            (-40, 69.28), 80, 0, 120, linewidth=shotzone_lw, color=shotzone_color)

        # Assume x distance is also 40 for the endpoint
        inner_line_3 = Rectangle(
            (53.20, 150.89), 290, 0, 70.53, linewidth=shotzone_lw, color=shotzone_color)
        inner_line_4 = Rectangle(
            (-53.20, 150.89), 290, 0, 109.47, linewidth=shotzone_lw, color=shotzone_color)

        # Assume y distance is also 92.5 for the endpoint
        inner_line_5 = Rectangle(
            (130.54, 92.5), 78, 0, 35.32, linewidth=shotzone_lw, color=shotzone_color)
        inner_line_6 = Rectangle(
            (-130.54, 92.5), 78, 0, 144.68, linewidth=shotzone_lw, color=shotzone_color)

        # ----------------------------------------------
        # 8 ft. 2 [1]
        inner_circle_shotzone = Circle(
            (0, 0), radius=80, linewidth=shotzone_lw, color=zone_colors[0], fill=True)

        # Center 16 ft. 2 [2]
        center_16ft_2_polygon = Polygon([[-79, 137],
                                         [-76, 140], [-67, 144], [-57, 149], [-53.2, 150.89], [-52,
                                                                                               151], [-44, 152], [-34, 155], [-24, 157], [-14, 158], [-4, 158],
                                         [4, 158], [14, 158], [24, 157], [34, 155], [44, 152], [
                                             52, 151], [53.2, 150.89], [57, 149], [67, 144], [76, 140],
                                         [79, 137], [39, 68],
                                         [32, 74], [23, 77], [12, 79], [
                                             2, 80], [-8, 79], [-19, 78], [-29, 75], [-39, 68],
                                         ], linewidth=shotzone_lw, color=zone_colors[1], fill=True)

        # Center 2 [3]
        center2_polygon = Polygon([[-52.2, 149.89],
                                   [-52, 151], [-44, 154], [-34, 157], [-24, 159], [-14, 160], [-4, 160], [
                                       6, 160], [17, 160], [27, 158], [36, 157], [44, 154], [51, 151],
                                   [52.2, 149.89], [79, 224],
                                   [79, 224], [73, 226], [66, 229], [56, 230], [47, 232], [37, 235], [27, 236], [19, 237], [9, 238], [
            0, 238], [-9, 238], [-17, 238], [-27, 237], [-37, 235], [-46, 233], [-55, 232], [-62, 229], [-70, 228], [-78, 225],
            [-79, 224]], linewidth=shotzone_lw, color=zone_colors[2], fill=True)

        # Center 3 [4]
        center3_polygon = Polygon([[-80, 225],
                                  [-78, 225], [-70, 228], [-62, 229], [-55, 232], [-46, 233], [-37, 235], [-27, 237], [-17, 238], [-9, 238], [
                                      0, 238], [9, 238], [19, 237], [27, 236], [37, 235], [47, 232], [56, 230], [66, 229], [73, 226], [79, 224],
                                  [80, 225], [150, 422.5], [-150, 422.5]], linewidth=shotzone_lw, color=zone_colors[3], fill=True)

        # Left 16 ft. 2 [5]
        left_16ft_2_polygon = Polygon([[-153, -47.5], [-64, -47.5],
                                       [-69, -40], [-74, -30], [-78, -19], [-79, -7], [-79, 4], [-78,
                                                                                                 17], [-75, 28], [-69, 39], [-62, 48], [-56, 56], [-48, 64], [-40, 69],
                                       [-80, 138], [-84, 136], [-92, 131], [-100, 125], [-109,
                                                                                         117], [-117, 109], [-124, 101], [-129, 94],
                                       [-133, 89], [-138, 80], [-144, 71], [-148, 60], [-152, 50], [-155, 38], [-157, 27], [-159, 16], [-160, 5], [-160, -5], [-159, -16], [-158, -27], [-155, -38]], linewidth=shotzone_lw, color=zone_colors[4], fill=True)

        # Left Center 2 [6]
        left_center2_polygon = Polygon([[-53.2, 150.89],
                                        [-57, 149], [-67, 146], [-76, 140], [-84, 136], [-92, 131], [-100,
                                                                                                     125], [-109, 117], [-117, 109], [-124, 101], [-129, 94],
                                        [-131, 94], [-195, 137],
                                        [-187, 146], [-182, 154], [-176, 160], [-170, 166], [-165,
                                                                                             172], [-160, 177], [-154, 182], [-148, 186], [-143, 190],
                                        [-80, 225]], linewidth=shotzone_lw, color=zone_colors[5], fill=True)

        # Left Center 3 [7]
        left3_polygon = Polygon([[-250, 93.5], [-220, 93.5],
                                 [-219, 93], [-216, 100], [-213, 106], [-210, 112], [-206, 118], [-203, 123], [-200, 128], [-196, 134], [-193, 140], [-189, 144], [-185, 149], [-180, 154], [-176, 160], [-172, 164], [-167,
                                                                                                                                                                                                                       168], [-163, 172], [-158, 177], [-153, 182], [-148, 186], [-143, 190], [-137, 195], [-131, 198], [-126, 202], [-120, 206], [-114, 209], [-108, 212], [-102, 215], [-95, 218], [-88, 221], [-82, 223],

                                 [-80, 225], [-150, 422.5], [-250, 422.5]], linewidth=shotzone_lw, color=zone_colors[6], fill=True)
        # Left Coner 2 [8]
        left_corner2_polygon = Polygon([[-218, -47.5], [-218, 92.5],
                                        [-211, 110], [-202, 125],
                                        [-195, 137], [-131, 92],
                                        [-133, 89], [-138, 80], [-144, 69], [-148, 60], [-152, 50], [-155, 38], [-156, 27], [-159, 16], [-160, 5], [-160, -5], [-159, -16], [-158, -27], [-155, -38], [-153, -47.5]], linewidth=shotzone_lw, color=zone_colors[7], fill=True)
        # Left Coner 3 [9]
        left_corner3_polygon = Polygon([[-250, -47.5], [-218, -47.5], [-218, 91.5],
                                       [-250, 91.5]], linewidth=shotzone_lw, color=zone_colors[8], fill=True)

        # Right 16 ft. 2 [10]
        right_16ft_2_polygon = Polygon([[153, -47.5], [64, -47.5],
                                        [69, -40], [74, -30], [78, -19], [79, -7], [79, 4], [78, 17], [
                                            75, 28], [69, 39], [62, 48], [56, 56], [48, 64], [40, 69],
                                        [80, 138], [84, 136], [92, 131], [100, 125], [
                                            109, 117], [117, 109], [124, 101], [129, 94],
                                        [133, 89],
                                        [138, 80], [144, 69], [148, 60], [
                                            152, 50], [155, 38],

                                        [157, 27], [159, 16], [160, 5], [160, -5], [159, -16], [156, -27], [155, -38]], linewidth=shotzone_lw, color=zone_colors[9], fill=True)

        # Right Center 2 [11]
        right_center2_polygon = Polygon([[53.2, 150.89],
                                         [57, 149], [67, 146], [76, 140], [84, 136], [92, 131], [
                                             100, 125], [109, 117], [117, 109], [124, 101], [129, 94],
                                         [131, 94], [195, 137],
                                         [187, 146], [182, 154], [176, 160], [170, 166], [165, 172], [
                                             160, 177], [154, 182], [148, 186], [143, 190],
                                         [80, 225]], linewidth=shotzone_lw, color=zone_colors[10], fill=True)

        # Right Center 3 [12]
        right3_polygon = Polygon([[220, 93.5],
                                  [219, 93], [216, 100], [213, 106], [210, 112], [206, 118], [203, 123], [200, 128], [196, 134], [193, 140], [189, 144], [185, 149], [180, 154], [176, 160], [172, 164], [167, 168], [
                                      163, 172], [158, 177], [153, 182], [148, 186], [143, 190], [137, 195], [131, 198], [126, 202], [120, 206], [114, 209], [108, 212], [102, 215], [95, 218], [88, 221], [82, 223],
                                  [80, 225], [150, 422.5], [250, 422.5], [250, 93.5]], linewidth=shotzone_lw, color=zone_colors[11], fill=True)

        # Right Coner 2 [13]
        right_corner2_polygon = Polygon([[220, -47.5], [220, 92.5],
                                         [211, 110], [202, 125],
                                         [195, 137], [131, 92],
                                         [133, 89], [138, 80], [144, 71], [148, 60], [152, 50], [155, 38], [157, 27], [159, 16], [160, 5], [160, -5], [159, -16], [158, -27], [155, -38], [153, -47.5]], linewidth=shotzone_lw, color=zone_colors[12], fill=True)
        # Right Coner 3 [14]
        right_corner3_polygon = Polygon([[250, -47.5], [220, -47.5], [220, 92.5], [
                                        250, 92.5]], linewidth=shotzone_lw, color=zone_colors[13], fill=True)

        # List of the court elements to be plotted onto the axes
        court_elements = [
            left_corner3_polygon, right_corner3_polygon, right_center2_polygon, right_corner2_polygon, right_16ft_2_polygon,
            left_center2_polygon, center2_polygon, center_16ft_2_polygon,
            center3_polygon, left3_polygon, right3_polygon, left_corner2_polygon, left_16ft_2_polygon, inner_circle_shotzone,
            outer_box, inner_box, top_free_throw,
            bottom_free_throw, restricted, corner_three_a,
            corner_three_b, three_arc, center_outer_arc,
            center_inner_arc, outer_circle, inner_circle,
            corner_three_a_x, corner_three_b_x,
            inner_line_1, inner_line_2, inner_line_3, inner_line_4, inner_line_5, inner_line_6
        ]
    else:
        # List of the court elements to be plotted onto the axes
        court_elements = [outer_box, inner_box, top_free_throw,
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
    FONT_SIZE = 14

    ax.text(0, 0, texts[0], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(0, 120, texts[1], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(0, 190, texts[2], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(0, 300, texts[3], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(-120, 0, texts[4], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(-110, 160, texts[5], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(-170, 300, texts[6], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(-180, 60, texts[7], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(-220, 0, texts[8], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(120, 0, texts[9], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(110, 160, texts[10], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(170, 300, texts[11], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(180, 60, texts[12], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))
    ax.text(220, 0, texts[13], fontsize=FONT_SIZE, fontweight='bold', horizontalalignment='center',
            verticalalignment='center').set_bbox(dict(color='white', alpha=0.2))

    from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)

    from PIL import Image

    # logo = Image.open(TEAMS_LOGO)
    # imagebox = OffsetImage(logo, zoom=TEAMS_LOGO_RATIO)
    # imagebox = OffsetImage(logo)
    # ab = AnnotationBbox(imagebox, (0, 380), frameon=False)
    # ax.add_artist(ab)

    return ax

def fix_missing_rows(data):

    COLUMNS = ['SHOT_ZONE_CUTSOM','SUM_SMF','COUNT_SMF','FPG']
    now_list = data['SHOT_ZONE_CUTSOM'].values.tolist()
    standard_list= ['8 ft. 2','Center 16 ft. 2','Center 2','Center 3','Left 16 ft. 2','Left Center 2','Left Center 3',
                'Left Coner 2','Left Coner 3','Right 16 ft. 2','Right Center 2','Right Center 3','Right Coner 2','Right Coner 3']
    
    missing_list = list (set(standard_list) - set(now_list))
    
    df_missing = pd.DataFrame(columns=COLUMNS)
    for missing_part in missing_list:
        df_missing = pd.concat([pd.DataFrame([[missing_part,0,0,0.0]], columns=COLUMNS), df_missing], ignore_index=True)
        # else:
            # df_missing = pd.concat([pd.DataFrame([[game_number,missing_part,0,0,0.0]], columns=COLUMNS), df_missing], ignore_index=True)
    
    data = pd.concat([data,df_missing], ignore_index=True)
    result = data.sort_values(by=['SHOT_ZONE_CUTSOM'])
    return result


@st.cache_data
def get_data():
    FILE_PATH = glob.glob(os.path.join(
        'D:/side_project/tk_test_1023/Api Data/*.csv'))
    df_from_each_file = (pd.read_csv(f, delimiter=',', index_col=0)
                         for f in FILE_PATH)
    df = pd.concat(df_from_each_file, ignore_index=True)
    return df


TEAMS_STYLE = [
    ['Braves',   ['#0080FF', '#46A3FF', '#84C1FF', '#97CBFF', '#ACD6FF',
                  '#D2E9FF', '#ECF5FF'], 'D:/side_project/tk_test_1023/Logo/BRAVES_LOGO.png', 0.5],
    ['Kings',    ['#FFC71F', '#FFFF37', '#FFFF5C', '#FFFF80', '#FFFFB3', '#FFFFD6',
                  '#FFFFF0'], 'D:/side_project/tk_test_1023/Logo/KINGS_LOGO.png', 0.22],
    ['Pilots',   ['#D14200', '#FF5405', '#FF7738', '#FF9A6B', '#FFBD9E', '#FFE0D1',
                  '#FFF8F5'], 'D:/side_project/tk_test_1023/Logo/PILOTS_LOGO.png', 0.6],
    ['Lioneers', ['#7000D1', '#8A05FF', '#A238FF', '#BA6BFF', '#D29EFF', '#EAD1FF',
                  '#FAF5FF'], 'D:/side_project/tk_test_1023/Logo/LIONEERS_LOGO.png', 0.6],
    ['Dreamers', ['#006327', '#008A37', '#00CC5E', '#3FD97D', '#A6EDC2', '#D4F7E2',
                  '#EAFBF1'], 'D:/side_project/tk_test_1023/Logo/DREAMERS_LOGO.png', 0.4],
    ['Steelers', ['#AE0000', '#FF0505', '#FF3838', '#FF6B6B', '#FF9E9E', '#FFD1D1',
                  '#FFF5F5'], 'D:/side_project/tk_test_1023/Logo/STEELERS_LOGO.png', 0.5]
]

# 🟥🟨🟦🟪🟩🟧

GAME_ID_INFO = [
    ['Braves',  ['G01 🟨🟦','G02 🟥🟦','G05 🟦🟩','G10 🟦🟪','G11 🟦🟩','G15 🟦🟥','G20 🟥🟦','G22 🟪🟦','G25 🟦🟨'] ],
    ['Kings' ,  ['G01 🟨🟦','G04 🟪🟨','G06 🟧🟨','G07 🟧🟨','G09 🟥🟨','G14 🟨🟥','G16 🟨🟧','G21 🟨🟧','G25 🟦🟨','G27 🟩🟨'] ],
    ['Pilots' , ['G06 🟧🟨','G07 🟧🟨','G12 🟧🟥','G16 🟨🟧','G18 🟪🟧','G19 🟩🟧','G21 🟨🟧','G23 🟥🟧','G26 🟧🟪'] ],
    ['Lioneers',['G04 🟪🟨','G08 🟩🟪','G10 🟦🟪','G13 🟪🟩','G18 🟪🟧','G22 🟪🟦','G26 🟧🟪','G28 🟥🟪'] ],
    ['Dreamers',['G03 🟥🟩','G05 🟦🟩','G08 🟩🟪','G11 🟦🟩','G13 🟪🟩','G17 🟩🟥','G19 🟩🟧','G24 🟥🟩','G27 🟩🟨'] ],
    ['Steelers',['G02 🟥🟦','G03 🟥🟩','G09 🟥🟨','G12 🟧🟥','G14 🟨🟥','G15 🟦🟥','G17 🟩🟥','G20 🟥🟦','G23 🟥🟧','G24 🟥🟩','G28 🟥🟪'] ],
]

TEAM_PLAYER_ID_INFO = [
    ['Braves',  [' ','#0 賴廷恩','#1 陳范柏彥','#2 巴爾菲特 (季中註銷)','#3 張宗憲','#5 強森','#6 吳永盛','#7 伊波卡','#8 周桂羽'
                 ,'#9 石門','#10 張文平','#11 洪楷傑','#12 林志傑','#13 林孟學','#14 蔡文誠','#15 謝宗融','#17 辛特力','#21 曾祥鈞'
                 ,'#24 簡廷兆','#32 塞瑟夫','#33 蔡鎮嶽','#99 布朗'] ],
    ['Kings' ,  [' ','#0 海登','#1 林書緯','#2 蘇培凱','#3 陳俊男','#4 李威廷','#5 牧倫斯','#6 楊敬敏','#7 林書豪','#9 李愷諺','#10 簡祐哲'
                 ,'#11 王柏智','#14 米歇爾','#17 蘇士軒','#19 林金榜','#24 洪志善','#33 安尼奎','#49 翟振皓','#50 戴維斯','#55 曼尼高','#72 林力仁'] ],
    ['Pilots' , [' ','#0 周儀翔','#1 丁恩迪','#2 陳昱瑞','#3 勞倫斯','#5 密克斯','#6 關達祐','#7 喬楚瑜','#9 李學林','#10 林子洧','#12 李家慷'
                 ,'#21 伯朗','#25 林正','#27 張鎮衙','#30 白曜誠','#42 沃許本','#55 塔克','#69 盧峻翔'] ],
    ['Lioneers',[' ','#0 張傑瑋','#1 施顏宗','#2 姜廣謙','#3 王子綱','#4 高國豪','#5 宋宇軒','#6 克拉','#7 曾柏喻','#8 朱雲豪','#9 田浩','#11 蕭順議'
                 ,'#12 李家瑞','#17 劉光尚','#20 周伯勳','#21 伊凡 (季中註銷)','#23 呂奇旻','#24 艾夫伯','#31 阿提諾','#32 歐獅傅 (季中註銷)','#42 盧冠軒','#55 霍立飛'] ],
    ['Dreamers',[' ','#0 陳振傑','#3 吳家駿','#5 麥卡洛','#6 貝札尼什維利','#7 林耀宗','#8 王振原','#10 丁冠皓','#11 林俊吉','#18 楊盛硯','#21 簡浩','#23 錢肯尼'
                 ,'#24 忻沃克','#26 李德威','#28 盧冠良','#30 吳松蔚','#34 吉爾貝克','#42 布依德','#88 周柏臣']],
    ['Steelers',[' ','#0 鐵米','#1 李睿麒','#2 劉承彥','#3 悟空 (季中註銷)','#4 陳又瑋','#6 邱柏璋','#8 王律翔','#11 比克 (季中註銷)','#13 呂政儒','#15 盧哲毅','#18 林郅為'
                 ,'#20 班尼特 (季中註銷)','#24 楊和','#28 施晉堯','#30 陳冠全','#34 塔壁','#35 丹尼爾','#77 張伯維'] ],
]


try:
    global teams

    iterations = st.sidebar.slider("投籃數量標準(含以上)", 2, 20, 10, 1)

    # if not teams:
    #     st.error("Please select one team.")
    # else :
    #     global game_number
    #     game_id_info = [ x for x in GAME_ID_INFO if x[0] == str(teams)]
    #     all = st.sidebar.checkbox("Select all games")

    #     if all:
    #         game_number = st.sidebar.multiselect("Choose Game Numbers", game_id_info[0][1],game_id_info[0][1])
    #     else:
    #         game_number = st.sidebar.multiselect("Choose Game Numbers", game_id_info[0][1])

    #     game_number = [item.split(' ')[0] for item in game_number]

    #     player_id_info = [ x for x in TEAM_PLAYER_ID_INFO if x[0] == str(teams)]
    #     player_id = st.sidebar.multiselect('Choose Players',player_id_info[0][1])
    #     # player_id = st.sidebar.selectbox('Choose One Player',player_id_info[0][1])
    #     # player_id = st.sidebar.text_input('pls input player number')


    with st.form(key='my_form'):
        submit_button = st.form_submit_button(label='產生')

        if submit_button:
            df = get_data()

            # if teams:
                # TEAM_STYLE_INFO = [x for x in TEAMS_STYLE if x[0] == str(teams)]
                # TEAMS_COLOR = TEAM_STYLE_INFO[0][1]
                # TEAMS_LOGO  = TEAM_STYLE_INFO[0][2]
                # TEAMS_LOGO_RATIO = TEAM_STYLE_INFO[0][3]

            FILTER_COL1 = ['TEAM_NAME','PLAYER_ID','SHOT_ZONE_CUTSOM']
            FILTER_COL2 = ['TEAM_NAME','PLAYER_ID','SHOT_ZONE_CUTSOM','SUM_SMF','COUNT_SMF']
            FILTER_COL3 = ['TEAM_NAME','PLAYER_ID','SHOT_ZONE_CUTSOM']

            braves =df

            braves['SUM_SMF']   = braves.groupby(FILTER_COL1)['SHOT_MADE_FLAG'].transform('sum')
            braves['COUNT_SMF'] = braves.groupby(FILTER_COL1)['SHOT_MADE_FLAG'].transform('count')
            braves = braves[FILTER_COL2]


            braves = braves.groupby(FILTER_COL3).agg({'SUM_SMF': max, 'COUNT_SMF': max})
            braves = braves.reset_index()
            braves['FPG'] = braves['SUM_SMF'] / braves['COUNT_SMF']
            ##################################
            FIILTER_SHOT_LIMIT = iterations
            ##################################
            QUERY = "COUNT_SMF >= " + str(FIILTER_SHOT_LIMIT)
            braves_filter = braves.query(QUERY)

            FILTER_COL4 = ['SHOT_ZONE_CUTSOM']

            idx = braves_filter.groupby(FILTER_COL4)['FPG'].transform('max') == braves_filter['FPG']
            braves_exp = braves_filter[idx]
            braves_exp.sort_values(['SHOT_ZONE_CUTSOM','FPG','COUNT_SMF'],ascending=[True, False, False], inplace=True)
            braves_exp['overall_rank'] = 1  
            braves_exp['overall_rank'] = braves_exp.groupby(['SHOT_ZONE_CUTSOM'])['overall_rank'].cumsum()
            braves_exp = braves_exp.query("overall_rank==1")
            braves_exp = braves_exp.drop("overall_rank",axis=1)

            braves_exp['Combined'] = braves_exp['TEAM_NAME'].astype(str) +" "+ braves_exp['PLAYER_ID'].astype(str) \
                            + '\n' + braves_exp['SUM_SMF'].astype(str) + '/' + braves_exp['COUNT_SMF'].astype(str) + '\n' \
                            + round(braves_exp['FPG']*100, 1).astype(str) + '%'

            if braves_exp.shape[0] != 14:
                    braves_exp = fix_missing_rows(braves_exp)


            conditions = [
                (braves_exp['TEAM_NAME'] == 'Braves'),
                (braves_exp['TEAM_NAME'] == 'Kings'),
                (braves_exp['TEAM_NAME'] == 'Pilots'),
                (braves_exp['TEAM_NAME'] == 'Lioneers'),
                (braves_exp['TEAM_NAME'] == 'Dreamers'),
                (braves_exp['TEAM_NAME'] == 'Steelers'),
                (braves_exp['TEAM_NAME'].isna())
            ]
            TEAMS_COLOR = ['#D2E9FF','#FFFFD6','#FFE0D1','#EAD1FF','#D4F7E2','#FFD1D1','#FFFFFF']
            braves_exp['FPG_RANK'] = np.select(conditions, TEAMS_COLOR)
            print(braves_exp.head(50))
            print('------------------------=')
            color_map = list(braves_exp['FPG_RANK'])
            # fpg_map   = list(round(test_df['FPG']*100,2))
            fpg_list = list(braves_exp['Combined'])

            demo = pd.DataFrame()

            # Set the size for our plots
            plt.rcParams['figure.figsize'] = (12, 11)

            # if len(player_id) != 0:
            #     TITLE = teams + '_' +  str(game_number) + '_' + str(player_id)
            # else:
            #     TITLE = teams + '_' +  str(game_number)

            TITLE='Shooting Number >= ' + str(FIILTER_SHOT_LIMIT)

            shot_chart(demo, title=TITLE,zone_colors=color_map, texts=fpg_list)

            st.pyplot(plt.gcf())

            # plt.savefig('shotzone.png', dpi=250,
            # bbox_inches='tight', pad_inches=0.05)

            # plt.show()
    # st.dataframe(braves_exp)

except URLError as e:
    st.error(
        """
            **This demo requires internet access.**
            Connection error: %s
        """
        % e.reason
    )
