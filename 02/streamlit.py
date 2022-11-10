# -*- coding: utf-8 -*-

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from sklearn.cross_decomposition import PLSRegression

def set_iris_data():
    df = px.data.iris()
    return df

def show_data_selection_bar(df):
    options = {'sepal_length': {}, 'sepal_width': {}}

    st.sidebar.title('Selector')
    species = df['species'].unique()
    selected_species = st.sidebar.multiselect(
        'Species', options=species, default=species)
    options['selected_species'] = selected_species

    min_value = df['sepal_length'].min().item()
    max_value = df['sepal_length'].max().item()
    sepal_len_min, sepal_len_max = st.sidebar.slider(
        'Sepal Length', 
        min_value=min_value, max_value=max_value,
        value=(min_value, max_value)
    )

    min_value = df['sepal_width'].min().item()
    max_value = df['sepal_width'].max().item()
    sepal_wid_min, sepal_wid_max = st.sidebar.slider(
        'Sepal Width', 
        min_value=min_value, max_value=max_value,
        value=(min_value, max_value)
    )

    options['sepal_length']['min'] = sepal_len_min
    options['sepal_length']['max'] = sepal_len_max
    options['sepal_width']['min'] = sepal_wid_min
    options['sepal_width']['max'] = sepal_wid_max

    return options
   
    
def show_dataframe(df):
    st.dataframe(df)


def show_scatterplot(df):
    # extract column names
    axis_list = df.columns.unique()
    # select X axis name
    selected_xaxis = st.selectbox(
        'X-axis', axis_list, 
    )
    # select Y axis name
    selected_yaxis = st.selectbox(
        'Y-axis', axis_list
    )
    # 
    fig = px.scatter(df, x=selected_xaxis, y=selected_yaxis, color="species")
    st.plotly_chart(fig, use_container_width=True)

def show_plsda(df):
    y = pd.get_dummies(df['species'], drop_first = True)
    pls = PLSRegression(n_components = 2)
    pls.fit(df.drop(['species', 'species_id'], axis = 1), y)
    scores = pd.DataFrame(pls._x_scores, index = df.index)
    scores['species'] = df['species']

    fig = px.scatter(scores, x = 0, y = 1, color = 'species')
    st.plotly_chart(fig, use_container_width=True)

    vips = calculate_vips(pls)
    vips_df = pd.DataFrame({'features': list(vips.keys()), 'vip': list(vips.values())})
    fig = px.bar(vips_df, x = 'features', y = 'vip')
    st.plotly_chart(fig, use_container_width=True)

def calculate_vips(model):
    t = model.x_scores_
    w = model.x_weights_
    q = model.y_loadings_
    p, h = w.shape
    vips = np.zeros((p,))
    s = np.diag(np.matmul(np.matmul(np.matmul(t.T,t),q.T), q)).reshape(h, -1)
    total_s = np.sum(s)
    for i in range(p):
        weight = np.array([ (w[i,j] / np.linalg.norm(w[:,j]))**2 for j in range(h) ])
        vips[i] = np.sqrt(p*(np.matmul(s.T, weight))/total_s)
    vips = {model.feature_names_in_[i]: vips[i] for i in range(len(vips))}
    return vips

def main():
    st.title('Iris Dataset Dashboard')
    df = set_iris_data()
    
    options = show_data_selection_bar(df)
    df_tmp = df[df['species'].isin(options['selected_species'])]
    df_selected = df_tmp[(df_tmp['sepal_length'] >= options['sepal_length']['min']) & 
                         (df_tmp['sepal_length'] <= options['sepal_length']['max']) &
                         (df_tmp['sepal_width'] >= options['sepal_width']['min']) &
                         (df_tmp['sepal_width'] <= options['sepal_width']['max'])]
    
    st.write("Before selection: %d rows, %d columns" % (df.shape[0], df.shape[1]))
    st.write("After selection: %d rows, %d columns" % (df_selected.shape[0], df_selected.shape[1]))
    st.subheader('Scatter Plot:')
    show_scatterplot(df_selected)
    st.subheader('Selected Data:')
    show_dataframe(df_selected)

    st.subheader("PLS-DA")
    show_plsda(df)



if __name__ == '__main__':
    main()