# Makefile
# Author: Sarah Abdelazim
# Date: 2023-01-06

# all : doc/final_report.html 

all : doc/final_project.html doc/final_project.md

clean : 
	rm -rf data/*
	rm -rf figures/*
	rm -f doc/final_project.html
	rm -f doc/final_project.md

# download raw data
data/raw/disney_characters.csv data/raw/disney_director.csv data/raw/--disney_movies_total_grosstotal-gross.csv data/raw/disney_revenue_1991_2016.csv data/raw/disney_voice_actors.csv : src/download_data.py
	python src/download_data.py --disney_characters=https://raw.githubusercontent.com/reisanar/datasets/master/disney-characters.csv --disney_director=https://raw.githubusercontent.com/uomodellamansarda/DisneyMoviesAnalysis/main/disney-director.csv --disney_movies_total_gross=https://raw.githubusercontent.com/uomodellamansarda/DisneyMoviesAnalysis/main/disney_movies_total_gross.csv --disney_revenue_1991_2016=https://raw.githubusercontent.com/uomodellamansarda/DisneyMoviesAnalysis/main/disney_revenue_1991-2016.csv --disney_voice_actors=https://raw.githubusercontent.com/uomodellamansarda/DisneyMoviesAnalysis/main/disney-voice-actors.csv --out_dir=data/raw/

# processing data
data/processed/disney_characters.csv data/processed/disney_director.csv data/processed/disney_movies_total_gross.csv data/processed/disney_revenue_1991_2016.csv data/processed/disney_voice_actors.csv : data/raw/disney_characters.csv data/raw/disney_director.csv data/raw/disney_movies_total_gross.csv data/raw/disney_revenue_1991_2016.csv data/raw/disney_voice_actors.csv src/preprocessing.py
	python src/preprocessing.py --disney_characters=data/raw/disney_characters.csv --disney_director=data/raw/disney_director.csv --disney_movies_total_gross=data/raw/disney_movies_total_gross.csv --disney_revenue_1991_2016=data/raw/disney_revenue_1991_2016.csv --disney_voice_actors=data/raw/disney_voice_actors.csv --out_dir=data/processed/

# eda files
data/figures/director_count.png data/figures/director_genres.png data/figures/genre_chart.png data/figures/genre_count.png data/figures/rating_count.png data/figures/revenue_chart.png data/figures/revenue_density.png data/figures/voice_actor_count.png data/figures/year_chart.png : data/processed/disney_characters.csv data/processed/disney_director.csv data/processed/disney_movies_total_gross.csv data/processed/disney_revenue_1991_2016.csv data/processed/disney_voice_actors.csv src/disney_eda.py
	python src/disney_eda.py --disney_characters=data/processed/disney_characters.csv --disney_director=data/processed/disney_director.csv --disney_movies_total_gross=data/processed/disney_movies_total_gross.csv --disney_revenue_1991_2016=data/processed/disney_revenue_1991_2016.csv --disney_voice_actors=data/processed/disney_voice_actors.csv --out_dir=data/figures/

# Render final report
doc/final_project.html : data/figures/director_count.png data/figures/director_genres.png data/figures/genre_chart.png data/figures/genre_count.png data/figures/rating_count.png data/figures/revenue_chart.png data/figures/revenue_density.png data/figures/voice_actor_count.png data/figures/year_chart.png doc/disney.bib
	Rscript -e "rmarkdown::render('doc/final_project.Rmd')"

doc/final_project.md : data/figures/director_count.png data/figures/director_genres.png data/figures/genre_chart.png data/figures/genre_count.png data/figures/rating_count.png data/figures/revenue_chart.png data/figures/revenue_density.png data/figures/voice_actor_count.png data/figures/year_chart.png doc/disney.bib
	Rscript -e "rmarkdown::render('doc/final_project.Rmd', output_format = 'github_document')"