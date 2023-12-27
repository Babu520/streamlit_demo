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

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

st.title('更新資訊')

st.markdown(
    """
    ## 2023-12-27
        - [數據] 比賽場次 G25 G26 G27 G28 已上傳
        - [修正] 球員號碼檢索體驗 ( 球員號碼 -> 球員號碼 中文名字)

        by BBG(小管)
    
    ## 操作說明
    """
)

from PIL import Image
img_test = Image.open('./images/demo_ui.jpg')

st.image(img_test, use_column_width=True)

try:
    print('hello')

except URLError as e:
    st.error(
        """
            **This demo requires internet access.**
            Connection error: %s
        """
        % e.reason
    )
