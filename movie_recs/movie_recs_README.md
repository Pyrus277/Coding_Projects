This program was a project from the 'Data Collection and Processing with Python' class
on Coursera, which is part of the Python 3 Specialization from the University of Michigan.

This is a movie recommendation program. 

Libraries used: requests, json.

Requires an OMDB api key to run-- see line 45 in the program.



This takes as input one or more movie titles from the user and returns a list of 
five recommended titles, ordered by their respective Rotten Tomatoes score. 

Specifically, the program takes the movies inputted by the user and then feeds them into the
TasteDive API to get five similar titles for each one as a JSON object. 
The program then parses this object and picks out just the titles and makes a list
of them.
Next, it feeds that list into the OMDB API which returns info on each title, including the
Rotten Tomatoes score, packaged in JSON.
Finally, the program parses this object, sorts all the movies by their RT scores, and returns 
only the five highest rated titles in descending order back to the user.

See comment lines in the program itself for even greater detail!
