# Superhero Movies Web Application
## Description
This is a web application that mainly used for superhero movies and superheroes. 

The home page shows the best 50 superhero movies. Users could choose one of them to see detail information, like the movies’ poster, box-office, release year, plot and main role’s power. Users can also search other movies by inputting the movie's name in the search bar, and then they will get detail information based on their query. When they look for the detail information of the movies and the superhero's power, users will be directed to different pages.

There is also a function that users could see the movies' box-office over the years, including not only the 50 best superhero movies, but also the movies that they search.

### Fuctions
- see 50 best superhero movies
- search for other movies
- see the movie's detail information
- see the power of superhero who is the main role in the movie
- see superhero movies' box-office over year
## Prerequisites
- Get an API key from the website [https://rapidapi.com/jakash1997/api/superhero-search](https://rapidapi.com/jakash1997/api/superhero-search)
- Required python packages
    - BeautifulSoup
    - imdb
    - sqlite3
    - Flask
    - plotly
    - pandas

## Structure
```
│  movies.sqlite
│  mycode.py
│  README.md
│  roles.json
│  .gitignore     
└─templates
       detail.html
       home.html
       plot.html
 ```
 ## Running the web application
 Run
 ```
 git clone https://github.com/yingkunm/SuperHero.git
 cd #the project directory
 python mycode.py
 ```
 Open 
 
 [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser

 ## Demo Link
 [https://youtu.be/80U71J7BqwA](https://youtu.be/80U71J7BqwA)
 
