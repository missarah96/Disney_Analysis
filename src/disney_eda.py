# author: Sarah Abdelazim
# date: 2022-12-24

"""Creates eda plots for the pre-processed disney data 

Usage: src/disney_eda.py --disney_characters=<disney_characters> --disney_director=<disney_director> --disney_movies_total_gross=<disney_movies_total_gross> --disney_revenue_1991_2016=<disney_revenue_1991_2016> --disney_voice_actors=<disney_voice_actors> --out_dir=<out_dir>
  
Options:
--disney_characters=<disney_characters>                     Path (including filename) to data 1 
--disney_director=<disney_director>                         Path (including filename) to data 2
--disney_movies_total_gross=<disney_movies_total_gross>     Path (including filename) to data 3
--disney_revenue_1991_2016=<disney_revenue_1991_2016>       Path (including filename) to data 4
--disney_voice_actors=<disney_voice_actors>                 Path (including filename) to data 5
--out_dir=<out_dir>                                         Path to directory where the plots should be saved
"""

import altair as alt
import numpy as np
import pandas as pd
import glob
import os
import sys
from textwrap import wrap
import vl_convert as vlc
from docopt import docopt

def save_chart(chart, filename, scale_factor=1):
    '''
    Save an Altair chart using vl-convert
    
    Parameters
    ----------
    chart : altair.Chart
        Altair chart to save
    filename : str
        The path to save the chart to
    scale_factor: int or float
        The factor to scale the image resolution by.
        E.g. A value of `2` means two times the default resolution.
    '''
    if filename.split('.')[-1] == 'svg':
        with open(filename, "w") as f:
            f.write(vlc.vegalite_to_svg(chart.to_dict()))
    elif filename.split('.')[-1] == 'png':
        with open(filename, "wb") as f:
            f.write(vlc.vegalite_to_png(chart.to_dict(), scale=scale_factor))
    else:
        raise ValueError("Only svg and png formats are supported")

def main(disney_characters, disney_director, disney_movies_total_gross, disney_revenue_1991_2016, disney_voice_actors, out_dir):
    
     # check if eda folder exists
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    
    # reads input file  
    disney_characters = pd.read_csv(disney_characters, parse_dates=['release_date'])
    disney_director = pd.read_csv(disney_director)
    disney_movies_total_gross = pd.read_csv(disney_movies_total_gross, parse_dates=['release_date'])
    disney_revenue_1991_2016 = pd.read_csv(disney_revenue_1991_2016, parse_dates=['Year'])
    disney_voice_actors = pd.read_csv(disney_voice_actors)

    
    # create merges
    merge_1 = disney_movies_total_gross.merge(disney_characters, on=["movie_title", "release_date"], how="outer")
    merge_2 = merge_1.merge(disney_director, on=['movie_title'], how="outer")
    listed_characters = disney_voice_actors.groupby(['movie_title']).agg({
        'character': lambda x: x.tolist(),
        'voice-actor': lambda x: x.tolist()})
    merge_3 = merge_2.merge(listed_characters, on=['movie_title'], how="outer")
    
    
    #create png file : count of genres 
    non_null_genres = merge_3[~merge_3['genre'].isnull()]
    
    genre_count = alt.Chart(non_null_genres).mark_bar().encode(
        x=alt.X('genre:N', sort='-y'),
        y=alt.Y('count()'), 
        color = 'genre')
    
    save_chart(genre_count, os.path.join(out_dir, 'genre_count.png'))
    
    
    #create png file: count of MPAA_rating
    non_null_rating = merge_3[~merge_3['MPAA_rating'].isnull()]
    
    rating_count = alt.Chart(non_null_rating).mark_bar().encode(
        x=alt.X('MPAA_rating:N', sort='-y'),
        y=alt.Y('count()'), 
        color = 'MPAA_rating')
    
    save_chart(rating_count, os.path.join(out_dir, 'rating_count.png'))
    
    
    #create png file : count of directors
    non_null_directors = merge_3[~merge_3['director'].isnull()]
    
    director_count = alt.Chart(non_null_directors).mark_bar().encode(
        x=alt.X('director:N', sort='-y'),
        y=alt.Y('count:Q'), 
        color=alt.Color('director:N')
    ).transform_aggregate(
        count='count()',
        groupby=['director']
    ).transform_window(
        rank='rank(count)',
        sort=[alt.EncodingSortField('count', order='descending')]
    ).transform_filter('datum.rank <= 10')
    
    save_chart(director_count, os.path.join(out_dir, 'director_count.png'))

    
    #create png file : distribution of two caterogrical columns (director and genre)
    non_null_director_genre = merge_3.dropna(subset=['genre', 'director'], how='any')
    
    director_genres = alt.Chart(non_null_director_genre).mark_circle().encode(
        x=alt.X('director'),
        y=alt.Y('genre'), 
        color = 'genre', size = 'count()')
    
    save_chart(director_genres, os.path.join(out_dir, 'director_genres.png'))

    
    #create png file : sum of total and inflation_adjusted gross per genre  
    genre_grouped = merge_3.groupby("genre").agg({"total_gross": "sum", "inflation_adjusted_gross": "sum"}).reset_index()
    genre_grouped = genre_grouped.melt(id_vars=['genre'], 
                              value_vars=['total_gross', 'inflation_adjusted_gross'], 
                              var_name='gross', 
                              value_name='value')
    genre_grouped['genre'] = genre_grouped['genre'].apply(wrap, args=[11])
    
    genre_chart = genre_chart = alt.Chart(genre_grouped).mark_bar().encode(
        x=alt.X('gross:N', axis=alt.Axis(title=None, labels=False, ticks=False)),
        y=alt.Y('value:Q', axis=alt.Axis(format='$~s')),
        color='gross:N',
        column=alt.Column('genre:N', sort=alt.EncodingSortField(field='value', op='mean', order='descending'),
                      header=alt.Header(title=None, labelOrient='bottom', labelAngle=0))
    ).configure_view(
        stroke='transparent').configure_axis(labelPadding=38, labelAlign='left')
    
    save_chart(genre_chart, os.path.join(out_dir, 'genre_chart.png'))
    
    
    #create png file : sum of total and inflation_adjusted gross per year  
    grouping2 = merge_3.groupby("release_date").agg({"total_gross": "sum", "inflation_adjusted_gross": "sum"}).reset_index()
    grouping2 = grouping2.melt(id_vars=['release_date'] , 
                               value_vars=['total_gross', 'inflation_adjusted_gross'], 
                               var_name='gross', 
                               value_name='value')
    grouping2 = grouping2[(grouping2['release_date'].dt.year >= 1991)]
    
    year_chart = alt.Chart(grouping2).mark_line().encode(
        x=alt.X('year(release_date):T'),
        y=alt.Y('sum(value):Q', axis=alt.Axis(format='$~s')),
        color='gross:N')
    
    save_chart(year_chart, os.path.join(out_dir, 'year_chart.png'))
    
    
  #create png file : total revenue line chart    
    revenue_chart = alt.Chart(disney_revenue_1991_2016).mark_line().encode(
        x = alt.X('Year', scale=alt.Scale(domain=('1991', '2016'))),
        y = alt.Y('Total', axis=alt.Axis(format='$~s')) 
    )
    save_chart(revenue_chart, os.path.join(out_dir, 'revenue_chart.png'))

    
    #create png file : count of voice actors
    none_null_voice_actors = disney_voice_actors[disney_voice_actors['voice-actor'] != 'None']
    
    voice_actor_count = alt.Chart(none_null_voice_actors).mark_bar().encode(
        x=alt.X('voice-actor:N', sort='-y'),
        y=alt.Y('count:Q'), 
        color=alt.Color('voice-actor:N')
    ).transform_aggregate(
        count='count()',
        groupby=['voice-actor']
    ).transform_window(
        rank='rank(count)',
        sort=[alt.EncodingSortField(field='count', order='descending')]
    ).transform_filter('datum.rank <= 10')
    
    save_chart(voice_actor_count, os.path.join(out_dir, 'voice_actor_count.png'))
    
    
    #create png file : density graph of all revenue types
    disney_revenue_melted = disney_revenue_1991_2016.melt(
        id_vars=['Year'] , 
        value_vars=['Studio Entertainment',
                    'Disney Consumer Products',
                    'Disney Interactive',
                    'Walt Disney Parks and Resorts',
                    'Disney Media Networks',
                    'Total'], 
        var_name='revenue', 
        value_name='value')
    
    revenue_density = alt.Chart(disney_revenue_melted).transform_density(
        'value',
        groupby=['revenue'],
        as_ = ['value', 'density'],
        steps=200,
        extent=[0,100000]
    ).mark_area(opacity=0.45).encode(
        alt.X('value:Q'),
        alt.Y('density:Q'),
        alt.Color('revenue:N')
    ).properties(width=400, height=400)
    
    save_chart(revenue_density, os.path.join(out_dir, 'revenue_density.png'))  
    
if __name__ == "__main__":
    try:
        opt = docopt(__doc__)
        main(opt["--disney_characters"], 
             opt["--disney_director"],
             opt["--disney_movies_total_gross"],
             opt["--disney_revenue_1991_2016"],
             opt["--disney_voice_actors"],
             opt["--out_dir"])
    except:
        print(__doc__)
