from bs4 import BeautifulSoup
import requests
import imdb
import json
import sqlite3
import time
from flask import Flask, render_template, request
import plotly.graph_objects as go
import plotly.express as px

app = Flask(__name__)


CACHE_FILENAME = "roles.json"

# create the sqlite database to store the movie 

# create_gender = '''
#     CREATE TABLE IF NOT EXISTS "Gender" (
# 			"Id"			INTEGER UNIQUE,
# 			"Name"		    TEXT NOT NULL,
# 			PRIMARY KEY ("Id" AUTOINCREMENT)
# 	);
# '''
# insert_gender_m = '''
#     INSERT INTO Gender
#     VALUES (Null, "male")
# '''
# insert_gender_f = '''
#     INSERT INTO Gender
#     VALUES (Null, "female")
# '''
# create_movies = '''
#     CREATE TABLE IF NOT EXISTS "Movie" (
# 			"Id"			INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
# 			"Name"			TEXT NOT NULL,
# 			"Year"			INTEGER NOT NULL,
# 			"Box_office"	INTEGER NOT NULL,
# 			"Production"	TEXT NOT NULL,
# 			"Poster"		TEXT NOT NULL,
# 			"Role"			TEXT NOT NULL,
#             "Plot"			TEXT NOT NULL,
# 			"Gender_Id"		INTEGER,
# 			FOREIGN KEY ( "Gender_Id" ) REFERENCES Gender( "Id" )
# 	);
# '''

# cur.execute(create_gender)
# cur.execute(create_movies)
# cur.execute(insert_gender_m)
# cur.execute(insert_gender_f)
# conn.commit()


# scrap the 50 best superhero movie web page
'''
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
'''

# Fetch the movies' detail information from an API, and then store the returned json in the database. 

# url = "http://www.omdbapi.com/?t="
# api_key = "&apikey=trilogy"
# movies_titles = title
# count = 0

# for i in movies_titles:
#     try:
#         response = requests.get(url + i + api_key)
#         data = response.json()
#         imdbID_v = data['imdbID']
#         id_v = imdbID_v[2:]
#         Title_v = data['Title']
#         Year_v = data['Year']
#         Production_v = data['Production']
#         BoxOffice_v = data['BoxOffice']
#         Plot_v = data['Plot']
#         Poster_v = data['Poster']
        
#         i =  imdb.IMDb(accessSystem='http')
#         movie = i.get_movie(id_v)
#         cast = movie['cast'][0]
                
#         if len(cast.currentRole) == 1:
#             Role1_v = str(cast.currentRole)
#             Role2_v = 'None'
#         elif len(cast.currentRole) == 2:
#             Role1_v = str(cast.currentRole[0])
#             Role2_v = str(cast.currentRole[1])
#         else:
#             Role1_v = 'None'
#             Role2_v = 'None'

#         insert_movie = '''
#             INSERT INTO Movie 
#             VALUES (Null,?, ?, ? ,? ,? ,? ,?, Null)
#           '''
#         movie_item = [Title_v, Year_v, BoxOffice_v, Production_v, Poster_v, Role1_v, Plot_v]
#         conn = sqlite3.connect("movies.sqlite")
#         cur = conn.cursor()
#         cur.execute(insert_movie, movie_item)
#         conn.commit()

#         print("=============")
#         print(count)
#         print(id_v)
#         print(f"Movie title: {Title_v}")
#         print(Year_v)
#         print(BoxOffice_v)
#         print(Production_v)
#         print(Poster_v)
#         print(f"{Role1_v} : {Role2_v}")
#         print("===end=====")
#         count +=1
    
#     except AttributeError as e:
#         print(e)



# Get the role's information from another API and store them in a json file.

# url = "https://superhero-search.p.rapidapi.com/api/"
# headers = {
#     'x-rapidapi-key': "9a6bf0e04fmsh79c2f42d9d6c2ddp17cf27jsn42eebafdf411",
#     'x-rapidapi-host': "superhero-search.p.rapidapi.com"
#     }

# conn = sqlite3.connect("movies.sqlite")
# cur = conn.cursor()
# query = "SELECT Role FROM Movie"
# result = cur.execute(query).fetchall()

# fw = open(CACHE_FILENAME,"a")
# cache_dict={}

# for i in result:
# 	querystring = {"hero":i[0]}
# 	try:
# 		response = requests.get(url, headers=headers, params=querystring)
# 		response = json.loads(response.text)
# 		gender_v = response['appearance']['gender']
# 		powerstars_v = response['powerstats']
# 		cache_dict[i[0]] = powerstars_v

# 		print(i[0])
# 		print(powerstars_v)

# 		update_movie = '''
# 			UPDATE Movie
# 			SET Gender_id = ?
# 			WHERE  Role = ?
# 		'''

# 		if gender_v == "Male":
# 			update_item = [1, i[0]]
# 		else:
# 			update_item = [2, i[0]]
# 		cur.execute(update_movie, update_item)
# 		conn.commit()
		
# 	except:
# 		print("Hero not found")
# 		update_item = [3, i[0]]
# 		cur.execute(update_movie, update_item)
# 		conn.commit()
# 	time.sleep(5)

# dumped_json_cache = json.dumps(cache_dict)
# fw.write(dumped_json_cache)

# fw.close() 
# conn.close()

def get_50_movies():
    conn = sqlite3.connect("movies.sqlite")
    cur = conn.cursor()
    q = '''
        SELECT Id, Name, Poster, Year, Box_office
        FROM Movie
        LIMIT 50
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

def get_detail_info(id):
    conn = sqlite3.connect("movies.sqlite")
    cur = conn.cursor()
    q = '''
        SELECT Id, Name, Year, Poster, Plot, Box_office, Role
        FROM Movie
    '''
    results = cur.execute(q).fetchall()
    result = []
    for i in results:
        if (str(i[0]) == id):
            result = i
            break
        else:
            continue
    conn.close()
    return result

def search_movie(name):
    conn = sqlite3.connect("movies.sqlite")
    cur = conn.cursor()

    find = 0
    q = '''
        SELECT Id, Name, Year, Poster, Plot, Box_office, Role
        FROM Movie
    '''
    results = cur.execute(q).fetchall()
    result = []
    for i in results:
        if (i[1].lower() == name.lower()):
            result = i
            find = 1
            break
        else:
            continue
    if find == 0:
        url = "http://www.omdbapi.com/?t="
        api_key = "&apikey=trilogy"
        response = requests.get(url + name + api_key)

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
        result = [0, Title_v, Year_v, Poster_v, Plot_v, BoxOffice_v, Role1_v]
        conn.close()
    return result

def get_role(role):
    url = "https://superhero-search.p.rapidapi.com/api/"
    headers = {
        'x-rapidapi-key': "9a6bf0e04fmsh79c2f42d9d6c2ddp17cf27jsn42eebafdf411",
        'x-rapidapi-host': "superhero-search.p.rapidapi.com"
        }
    
    conn = sqlite3.connect("movies.sqlite")
    cur = conn.cursor()
    cache_file = open(CACHE_FILENAME,"r")
    cache_contents = cache_file.read()
    cache_dict = json.loads(cache_contents)
    cache_file.close()
    find = 0
    for i in cache_dict:
        if role == i:
            character = cache_dict[i]
            find = 1
            break
        else:
            continue
    if(find == 0):
        print(role)
        querystring = {"hero": role}
        response = requests.get(url, headers=headers, params=querystring)
        try:
            response = json.loads(response.text)
            gender_v = response['appearance']['gender']
            powerstars_v = response['powerstats']
            cache_dict[role] = powerstars_v
            character = powerstars_v

            update_movie = '''
                UPDATE Movie
                SET Gender_id = ?
                WHERE  Role = ?
            '''
            if gender_v == "Male":
                update_item = [1, role]
            else:
                update_item = [2, role]
            cur.execute(update_movie, update_item)
            conn.commit()

        except:
            print("Hero not found")
            character = "sorry! Can not find the role!"
            cache_dict[role] = "sorry! Can not find the role!"

        fw = open(CACHE_FILENAME,"w")
        dumped_json_cache = json.dumps(cache_dict)
        fw.write(dumped_json_cache)

        cache_file.close() 
        conn.close()
    return character

def get_movies():
    conn = sqlite3.connect("movies.sqlite")
    cur = conn.cursor()
    q = '''
        SELECT Id, Name, Poster, Year, Box_office
        FROM Movie
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results


    


@app.route('/')
def index():
    results = get_50_movies()
    return render_template('home.html', results=results)

@app.route('/detail/<id>')
def detail(id):
    result = get_detail_info(id)
    power = get_role(result[6])
    name = result[6].replace(' ','')
    return render_template('detail.html', result=result, power=power, name=name)

@app.route('/handle_form', methods=['POST'])
def handle_search():
    movie_name = request.form["movie_name"]
    result = search_movie(movie_name)
    power = get_role(result[6])
    name = result[6].replace(' ','')
    return render_template('detail.html', result=result, power=power, name=name)

@app.route('/role/<name>')
def role_power(name):
    power = get_role(name)
    x_val = []
    y_val = []
    for i in power:
        x_val.append(i)
        y_val.append(power[i])
    bars_data = go.Bar(x=x_val, y=y_val)
    basic_layout = go.Layout(title=name + "\'s power")
    fig = go.Figure(data=bars_data, layout=basic_layout)
    div = fig.to_html(full_html=False)
    return render_template('plot.html', plot_div=div)

@app.route('/boxoffice')
def box_office():
    df = get_movies()
    x_val = []
    y_val = []
    name_val = []
    for i in df:
        x_val.append(i[3])
        t = i[4][1:]
        t = t.replace(',','')
        y_val.append(int(t))
        name_val.append(i[1])
    print(x_val)
    print("--------------------------------")
    print(y_val)
    fig = px.scatter(x=x_val, y=y_val, size=y_val, color=y_val,
           hover_name=name_val, log_x=True, size_max=60)
    fig.update_xaxes(title_text='year')
    fig.update_yaxes(title_text='Box Office ($)')
    fig.update_layout(
        title={
            'text':'Box Office Over Time',
            'y':0.95,
            'x':0.4,
            'xanchor': 'center',
            'yanchor': 'top'}
    )
    div = fig.to_html(full_html=False)
    return render_template('plot.html', plot_div=div)




if __name__ == '__main__':
    print('starting Flask app', app.name)
    app.run(debug=True)