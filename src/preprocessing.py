# author: Sarah Abdelazim
# date: 2022-12-24

"""Cleans and parses disney data.

Usage: preprocessing.py --disney_characters=<disney_characters> --disney_director=<disney_director> --disney_movies_total_gross=<disney_movies_total_gross> --disney_revenue_1991_2016=<disney_revenue_1991_2016> --disney_voice_actors=<disney_voice_actors> --out_dir=<out_dir> 
 
Options:
--disney_characters=<disney_characters>                     Path (including filename) to data 1 
--disney_director=<disney_director>                         Path (including filename) to data 2
--disney_movies_total_gross=<disney_movies_total_gross>     Path (including filename) to data 3
--disney_revenue_1991_2016=<disney_revenue_1991_2016>       Path (including filename) to data 4
--disney_voice_actors=<disney_voice_actors>                 Path (including filename) to data 5
--out_dir=<out_dir>                                         Path of where to locally write the file
"""

import os
import pandas as pd
import numpy as np
from docopt import docopt

opt = docopt(__doc__)

def main(disney_characters, disney_director, disney_movies_total_gross, disney_revenue_1991_2016, disney_voice_actors, out_dir):
    
    # make the output directory
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    #reads disney-characters file
    disney_characters = pd.read_csv(disney_characters, parse_dates=['release_date'])
    disney_characters.replace('\n','', regex=True, inplace=True)
    disney_characters.replace('', np.nan, inplace=True)
    disney_characters['release_date'].mask(disney_characters['movie_title'] == 'Aladdin', '1992-11-01', inplace=True)
    disney_characters.to_csv(os.path.join(out_dir, "disney_characters.csv"), date_format='%Y-%m', index=False)
        
        
    #reads disney_director file
    disney_director = pd.read_csv(disney_director)
    disney_director.rename(columns={"name":"movie_title"}, inplace=True)
    disney_director.drop(disney_director.index[[2,37]], inplace=True) #director name for the two Fantasia movies is vague
    disney_director.to_csv(os.path.join(out_dir, "disney_director.csv"), index=False)
    
    
    #reads disney_movies_total_gross file
    disney_movies_total_gross = pd.read_csv(disney_movies_total_gross, parse_dates=['release_date'])
    disney_movies_total_gross["total_gross"] = disney_movies_total_gross["total_gross"].replace("[$,]", "", regex=True).astype(float)
    disney_movies_total_gross["inflation_adjusted_gross"] = disney_movies_total_gross["inflation_adjusted_gross"].replace(
        "[$,]", "", regex=True).astype(float)
    disney_movies_total_gross['release_date'].mask(disney_movies_total_gross['movie_title'] == 'Aladdin', '1992-11-01', inplace=True)
    disney_movies_total_gross.loc[15, 'release_date'] = '1970-12-24'
    disney_movies_total_gross.loc[391, 'release_date'] = '2003-11-01'
    disney_movies_total_gross.loc[491, 'release_date'] = '2009-12-11'
    disney_movies_total_gross.loc[194, 'movie_title'] = 'The Jungle Book (b)'
    disney_movies_total_gross.loc[494, 'movie_title'] = 'Alice in Wonderland (b)'
    disney_movies_total_gross.loc[567, 'movie_title'] = 'The Jungle Book (c)'
    disney_movies_total_gross.loc[556, 'movie_title'] = 'Cinderella (b)'
    disney_movies_total_gross.loc[252, 'movie_title']  = '101 Dalmatians (b)'
    disney_movies_total_gross.loc[386, 'movie_title'] = 'Freaky Friday (b)'
    disney_movies_total_gross.loc[364, 'movie_title'] = 'Bad Company (b)'
    disney_movies_total_gross.to_csv(os.path.join(out_dir, "disney_movies_total_gross.csv"), date_format='%Y-%m', index=False)
    
    
    #reads disney_revenue_1991_2016 file
    disney_revenue_1991_2016 = pd.read_csv(disney_revenue_1991_2016, parse_dates=['Year'])
    disney_revenue_1991_2016.rename(
        columns={
        "Studio Entertainment[NI 1]": "Studio Entertainment",
        "Disney Consumer Products[NI 2]": "Disney Consumer Products",
        "Disney Interactive[NI 3][Rev 1]": "Disney Interactive"
        }, inplace=True)
    disney_revenue_1991_2016.to_csv(os.path.join(out_dir, "disney_revenue_1991_2016.csv"), index=False)
    
    
    #reads disney-voice-actors file
    disney_voice_actors = pd.read_csv(disney_voice_actors)
    disney_voice_actors.rename(columns={"movie":"movie_title"}, inplace=True)
    disney_voice_actors.to_csv(os.path.join(out_dir, "disney_voice_actors.csv"), index=False)

    
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
