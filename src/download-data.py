# author: Sarah Abdelazim
# date: 2022-12-24

"""Downloads csv data from the web to a local filepath as a csv.
Usage: download_data.py --disney_characters=<url_1> --disney_director=<url_2> --disney_movies_total_gross=<url_3> --disney_revenue_1991_2016=<url_4> --disney_voice_actors=<url_5> --out_dir=<out_dir> 
 
Options:
--disney_characters=<url_1>             URL from where to download the data (must be in standard csv format)
--disney_director=<url_2>               URL from where to download the data (must be in standard csv format)
--disney_movies_total_gross=<url_3>     URL from where to download the data (must be in standard csv format)
--disney_revenue_1991_2016=<url_4>      URL from where to download the data (must be in standard csv format)
--disney_voice_actors=<url_5>           URL from where to download the data (must be in standard csv format)
--out_dir=<out_dir>                     Path of where to locally write the file
"""

import os
import pandas as pd
from docopt import docopt

opt = docopt(__doc__)

def main(disney_characters, disney_director, disney_movies_total_gross, disney_revenue_1991_2016, disney_voice_actors, out_dir):
    
    # make the output directory
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
        
    #reads disney-characters file
    disney_characters = pd.read_csv(url_1)
    try:
        disney_characters.to_csv(os.path.join(out_dir, "disney-characters.csv"), index=False)
    except:
        os.makedirs(os.path.dirname(out_dir))
        disney_characters.to_csv(out_dir, index=False)
    
    
    #reads disney_director file
    disney_director = pd.read_csv(url_2)
    try:
        disney_director.to_csv(os.path.join(out_dir, "disney_director.csv"), index=False)
    except:
        os.makedirs(os.path.dirname(out_dir))
        disney_director.to_csv(out_dir, index=False)
    
    
    #reads disney_movies_total_gross file
    disney_movies_total_gross = pd.read_csv(url_3)
    try:
        disney_movies_total_gross.to_csv(os.path.join(out_dir, "disney_movies_total_gross.csv"), index=False)
    except:
        os.makedirs(os.path.dirname(out_dir))
        disney_movies_total_gross.to_csv(out_dir, index=False)
    
    
    #reads disney_revenue_1991_2016 file
    disney_revenue_1991_2016 = pd.read_csv(url_4)
    try:
        disney_revenue_1991_2016.to_csv(os.path.join(out_dir, "disney_revenue_1991_2016.csv"), index=False)
    except:
        os.makedirs(os.path.dirname(out_dir))
        disney_revenue_1991_2016.to_csv(out_dir, index=False)
    
    
    #reads disney_voice_actors file
    disney_voice_actors = pd.read_csv(url_5)
    try:
        disney_voice_actors.to_csv(os.path.join(out_dir, "disney_voice_actors.csv"), index=False)
    except:
        os.makedirs(os.path.dirname(out_dir))
        disney_voice_actors.to_csv(out_dir, index=False)

        
        
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

