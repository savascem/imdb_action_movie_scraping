# import

import requests as r
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import Request, urlopen
import urllib.request



## Target variables that I want to perform scraping on

title = []  # html tag -->>  'a'     / class -->> lister-item-header
link = []  # html tag -->>  'a'     / class -->> lister-item-header
year = []  # html tag -->>  'span'  / class -->> lister-item-year
runtime = []  # html tag -->>  'span'  / class -->> runtime
genre = []  # html tag -->>  'span'  / class -->> genre
rate = []  # html tag -->>  'div'   / class -->> ratings-imdb-rating
director = []  # html tag -->>   p(3)   / class -->> lister-item-content
storyline = []  # html tag -->>  'p'     / class -->> text-muted



## When you execute this function, will be add target variables to their respective lists.

def imdb_action_movies():

    url = "https://www.imdb.com/search/title/?title_type=feature&num_votes=10000,&genres=action&languages=en&start={}&explore=genres&ref_=adv_nxt/title/tt1630029/"

    # The page numbers increase by 50's.
    # I wrote a loop to traverse all the pages as 'page_number'.
    # Then, I wrote another loop that I can traverse as 'item' inside each page.

    for page_number in range(1, 2052, 50):

        if page_number <= 2051:

            url_ = url.format(page_number)
            data = r.get(url_)
            data_content = BeautifulSoup(data.content, 'html.parser')

            for item in range(0,50):

                #title
                titl_ = data_content.find_all("h3", {"class":"lister-item-header"})
                if item < len(titl_):
                    titl = titl_[item].a.get_text()
                    title.append(titl)

                    #link
                    link_ = "https://www.imdb.com/" + titl_[item].a.get("href")
                    link.append(link_)

                #year
                year_ = data_content.find_all("span", {"class":"lister-item-year"})
                if item < len(year_):
                    years = year_[item].get_text()
                    year.append(years)

                #runtime
                runtime_ = data_content.find_all("span", {"class":"runtime"})
                if item < len(runtime_):
                    runtimes = runtime_[item].get_text()
                    runtime.append(runtimes)

                #genre
                genre_ = data_content.find_all("span", {"class":"genre"})
                if item < len(genre_):
                    genres = genre_[item].get_text()
                    genre.append(genres)

                #ratings-imdb-rating
                rate_ = data_content.find_all("div", {"class":"ratings-imdb-rating"})
                if item < len(rate_):
                    rates = rate_[item].strong.get_text()
                    rate.append(rates)

                #director
                director_ = data_content.find_all("p", {"class": ""})
                if item < len(director_):
                    directors = director_[item].a.get_text()
                    director.append(directors)

            for item in range(1,100,2):

                #storyline
                story_ = data_content.find_all("p", {"class": "text-muted"})
                if item < len(story_):
                    story_s = story_[item].get_text()
                    storyline.append(story_s)

        else:
            break

imdb_action_movies()


## This function will be create a dataframe

def create_df():
    df = pd.DataFrame(columns=["title","year","runtime","genre","rate","director","storyline","link"])
    df["title"] = title
    df["year"] = year
    df["runtime"] = runtime
    df["genre"] = genre
    df["rate"] = rate
    df["director"] = director
    df["storyline"] = storyline
    df["link"] = link
    return df

dff = create_df()
