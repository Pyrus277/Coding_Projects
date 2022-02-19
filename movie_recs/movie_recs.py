
import requests
import json

#This function pulls info on 5 movies that are similar to what is inputted
#by the user, in a JSON object.
def get_movies_from_tastedive(title_str):
    baseurl = "https://tastedive.com/api/similar"
    paramsdict = {}
    paramsdict['q'] = title_str
    paramsdict['type'] = 'movies'
    paramsdict['limit'] = '5'
    TDresp = requests.get(baseurl, params = paramsdict)
    return TDresp.json() #makes a JSON object

#This pulls just the titles of the movies from the JSON returned by the function above.
def extract_movie_titles(movie_str):
    title_list = []
    movie_dict = movie_str
    for item in movie_dict['Similar']['Results']:
        title_list.append(item['Name'])
    return title_list

#This function takes a list of movies, and using the functions above, returns
#five movies for each title inputted
def get_related_titles(movie_list):
    related_list = []
    for movie in movie_list:
        sub_list = extract_movie_titles(get_movies_from_tastedive(movie))
        for item in sub_list:
            if item in related_list:
                continue
            else:
                related_list.append(item)
    return related_list

##############

#This returns movie info from OMDB as a JSON object
def get_movie_data(omdb_srch_str):
    baseurl = "http://www.omdbapi.com/"
    omdb_dict = {}
    omdb_dict["t"] = omdb_srch_str
    omdb_dict["r"] = "json"
    omdb_dict["apikey"] = "<ENTER API KEY HERE>"
    OMresp = requests.get(baseurl, params = omdb_dict)
    #print(OMresp.url)
    return OMresp.json()

#This pulls the Rotten Tomatoes score from the JSON returned by OMDB
def get_movie_rating(OMdict):
    rt = 0
    for rating in OMdict['Ratings']:
        if rating['Source'] == 'Rotten Tomatoes':
            rtscore = int((rating['Value'])[:2])
            return(rtscore)
            rt = 1
    if rt == 0:
        return(0)

#This function sorts the movies based on their rotten tomatoes scores,
#and in the case of a tie, alphabetically
def get_sorted_recommendations(movie_list):
    movies = get_related_titles(movie_list)
    movie_rating_dict = {}
    for movie in movies:
        movie_info_dict = get_movie_data(movie)
        movie_rating = get_movie_rating(movie_info_dict)
        movie_rating_dict[movie] = movie_rating
    final_list = []
    for movie in sorted(movie_rating_dict.keys(), key=lambda x: (-movie_rating_dict[x], movie_rating_dict)):
        final_list.append(movie)
    return final_list

#Code for the user interaction
user_favorites = []
user = ""
print("What are your favorite movies? \nEnter titles, and when finished, press 'q' and 'enter' to continue and get your results.\n")
while user != "q":
    user = input("")
    user_favorites.append(user)
recommendations = get_sorted_recommendations([user_favorites])
if recommendations == []:
    print("Sorry, I don't have any recommendations based on that. Try again.")
else:
    print("\nHere are some recommended movies:\n")
    for movie in recommendations:
        print(movie)
