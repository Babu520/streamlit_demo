import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="P+ League Shooting Stat",
    page_icon="📈",
)

st.write("# Welcome to P+ League Shooting Stat! 👋")

st.markdown(
    """
    ### 靈感來源
    - 主要參考     [NBA API](https://github.com/swar/nba_api)  
    - 數據欄位參考 [Shot_Chart_Detail](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/shotchartdetail.md)
"""
)

from PIL import Image
img_test = Image.open('./images/column_info.jpg')
# st.image(img_test)

img_test2 = Image.open('./images/shot_zone_custom_demo.jpg')
# st.image(img_test2)

images = [img_test,img_test2]

st.image(images, use_column_width=True)

