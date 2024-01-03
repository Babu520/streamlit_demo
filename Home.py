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

from PIL import Image
img_test = Image.open("./images/2024-01-03.jpg")
st.image(img_test, use_column_width=True)

st.title('更新資訊')
st.markdown(
    """
    ## 2023-12-28
        - [數據] 比賽場次 G29 G30 G31 G32
        - [修正] {Team Shot Zone}球員名稱錯誤(#42 沃許本)
        - [新增] {Rank} 各投籃區域排名

        by BBG(小管)
    ## 操作說明
    """
)


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
