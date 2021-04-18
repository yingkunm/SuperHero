from bs4 import BeautifulSoup
import requests
import imdb
import json
import sqlite3
import time

CACHE_FILENAME = "Roles.json"

conn = sqlite3.connect("movies.sqlite")
cur = conn.cursor()

create_gender = '''
    CREATE TABLE IF NOT EXISTS "Gender" (
			"Id"			INTEGER UNIQUE,
			"Name"		    TEXT NOT NULL,
			PRIMARY KEY ("Id" AUTOINCREMENT)
	);
'''
insert_gender_m = '''
    INSERT INTO Gender
    VALUES (Null, "male")
'''
insert_gender_f = '''
    INSERT INTO Gender
    VALUES (Null, "female")
'''
create_movies = '''
    CREATE TABLE IF NOT EXISTS "Movie" (
			"Id"			INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			"Name"			TEXT NOT NULL,
			"Year"			INTEGER NOT NULL,
			"Box-office"	INTEGER NOT NULL,
			"Production"	TEXT NOT NULL,
			"Poster"		TEXT NOT NULL,
			"Role"			TEXT NOT NULL,
            "Plot"			TEXT NOT NULL,
			"Gender_Id"		INTEGER,
			FOREIGN KEY ( "Gender_Id" ) REFERENCES Gender( "Id" )
	);
'''
cur.execute(create_gender)
cur.execute(create_movies)
cur.execute(insert_gender_m)
cur.execute(insert_gender_f)
conn.commit()


url = 'http://superheroes.theringer.com/?_ga=2.205407573.49282893.1583382995-1394544322.1583382995'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
results = soup.find_all('li', class_='card-item')

rank = []
title= []
boxOffice= []

for result in results:
    try:
        title_v = result.find('span', class_="title").text
        rank_v = result.find('div', class_="rank").span.text
        boxOfficeB = result.find('div', class_='expanded-data-col adjusted')
        boxOffice_v = boxOfficeB.find('span', class_='data offset').text

        rank.append(rank_v)
        title.append(title_v)
        boxOffice.append(boxOffice_v)
    except AttributeError as e:
        print(e)



url = "http://www.omdbapi.com/?t="
api_key = "&apikey=trilogy"
movies_titles = title
count = 0

for i in movies_titles:
    try:
        response = requests.get(url + i + api_key)
        data = response.json()
        imdbID_v = data['imdbID']
        id_v = imdbID_v[2:]
        Title_v = data['Title']
        Year_v = data['Year']
        Production_v = data['Production']
        BoxOffice_v = data['BoxOffice']
        Plot_v = data['Plot']
        Poster_v = data['Poster']
        
        i =  imdb.IMDb(accessSystem='http')
        movie = i.get_movie(id_v)
        cast = movie['cast'][0]
                
        if len(cast.currentRole) == 1:
            Role1_v = str(cast.currentRole)
            Role2_v = 'None'
        elif len(cast.currentRole) == 2:
            Role1_v = str(cast.currentRole[0])
            Role2_v = str(cast.currentRole[1])
        else:
            Role1_v = 'None'
            Role2_v = 'None'

        insert_movie = '''
            INSERT INTO Movie 
            VALUES (Null,?, ?, ? ,? ,? ,? ,?, Null)
		  '''
        movie_item = [Title_v, Year_v, BoxOffice_v, Production_v, Poster_v, Role1_v, Plot_v]
        cur.execute(insert_movie, movie_item)
        conn.commit()

        print("=============")
        print(count)
		print(id_v)
        print(f"Movie title: {Title_v}")
        print(Year_v)
		print(BoxOffice_v)
        print(Production_v)
		print(Poster_v)
        print(f"{Role1_v} : {Role2_v}")
        print("===end=====")
        count +=1
    
    except AttributeError as e:
        print(e)




url = "https://superhero-search.p.rapidapi.com/api/"
headers = {
    'x-rapidapi-key': "9a6bf0e04fmsh79c2f42d9d6c2ddp17cf27jsn42eebafdf411",
    'x-rapidapi-host': "superhero-search.p.rapidapi.com"
    }

conn = sqlite3.connect("movies.sqlite")
cur = conn.cursor()
query = "SELECT Role FROM Movie"
result = cur.execute(query).fetchall()

fw = open(CACHE_FILENAME,"a")
cache_dict={}

for i in result:
	print("=============================")
	querystring = {"hero":i[0]}
	try:
		response = requests.get(url, headers=headers, params=querystring)
		response = json.loads(response.text)
		gender_v = response['appearance']['gender']
		powerstars_v = response['powerstats']
		cache_dict[i[0]] = powerstars_v

		print(i[0])
		print(powerstars_v)

		update_movie = '''
			UPDATE Movie
			SET Gender_id = ?
			WHERE  Role = ?
		'''

		if gender_v == "Male":
			update_item = [1, i[0]]
		else:
			update_item = [2, i[0]]
		cur.execute(update_movie, update_item)
		conn.commit()
		
	except:
		print("Hero not found")
		update_item = [3, i[0]]
		cur.execute(update_movie, update_item)
		conn.commit()
	time.sleep(5)

dumped_json_cache = json.dumps(cache_dict)
fw.write(dumped_json_cache)

fw.close() 
conn.close()