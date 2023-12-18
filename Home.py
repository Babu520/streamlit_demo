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

st.title('👋👋👋')

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
