import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", page_title="Layering Analyzer")

if not 'combos_df' in st.session_state.keys():
    st.session_state['combos_df'] = None



st.title("Layering Analyzer")

upload_file = st.file_uploader(label='CSV File To Import', type=['csv'])


def perform_analysis():
    st.session_state['analyzed'] = True
    st.toast("analyzing...")
    limited_df = df[cols]
    arr = limited_df.values.tolist()
    limited_df = pd.DataFrame(arr)

    distinct_names = set([item for sublist in arr for item in sublist])

    combo_list = []

    for name in distinct_names:
        for inner in arr:
            if name in inner:
                for other_name in inner:
                    if name != other_name:
                        combo_list.append([name, other_name])

    combos_df = pd.DataFrame(combo_list)

    combos_df = combos_df.groupby([limited_df.columns[0], limited_df.columns[1]]).size().reset_index(name='count')
    combos_df = combos_df.sort_values(by="count", ascending=False)

    st.session_state['combos_df'] = combos_df
    st.toast("analysis completed!")


with st.expander('Upload Data', expanded=True):
    if upload_file is not None:
        df = pd.read_csv(upload_file)
        with st.container(border=True):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.dataframe(df.head(10), hide_index=True, use_container_width=True)
            with c2:
                cols = st.multiselect(options=df.columns,
                                      label="Columns to use for layering / commonality analysis")

        st.button("Perform Commonality Analysis", on_click=perform_analysis)

if st.session_state.get('analyzed', False) and upload_file:
    with st.expander('Output Data', expanded=True):
        st.dataframe(st.session_state['combos_df'])