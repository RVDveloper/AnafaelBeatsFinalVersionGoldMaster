from flask import Flask, redirect, url_for, request, render_template, jsonify
from youtube_search import YoutubeSearch
import os
import requests
import mysql.connector
import random
import pandas as pd
import datetime



#---------------------------Listas de API KEYS -------------------------------------------
#-----------------------------------------------------------------------------------------

Recomended_Songs=[

    "848aa0fb88mshfcc9267b32029a7p128ca3jsn4b6b5e842f9c",
    "3727704a2dmsh435e26b6bb980c4p19e0e3jsnb9a67df844f0",
    "2eb42c8091mshd82395a5ac85b21p186ea6jsnd01df2f95ef9",
    "449ce8e130mshab7119440a9202bp1c7ed1jsnfad742fec70a"

]
Recomended_ARTIST=[
    
    "b2679c01f4msha73bee93f6dd713p1baa6cjsn04757b1049fe",
    "8882e9b52dmshdf757077d18317cp1669e3jsnd6a38320d30d",
    "8bd169d58emsh3bdcea6eab336c7p14b237jsn6ad41d72fc31",
    "d908a968c9mshc580624ffe06e01p1a2620jsnad64847de84d"
]
Recomended_ALBUM=[
    
    "a2b400be88msh63c9ba83ee4c63cp158ac0jsnc1bd94e46518",
    "3bda4ddd3amsh4cc4a51d6a09dc2p1601bbjsn791a54b7dafe",
    "9f2e3a79b6msh642cda18856878ap187279jsnf8f3aa9a4600",
    "a74ea39549mshf57c0c5a5ce9b3fp1e1d88jsn4004260d7fc0"

]
Search_songs=[

    "b778861137msha9552ee7cb9a78cp1e8314jsn7d6bee4df576",
    "464f5199a1mshff5f113a3550551p1ec65ejsn0ca3e72f56eb"

]
download_Video=[
    
    "7b82371966msh7c1044dce74a4fcp18f5b1jsn5f416d907304",
    "b53263bf4cmsh134ff0e2dc35908p15cbf3jsne10e199296ee"
    
]




#?----------------------- Preguntas Random -----------------------------------------------


Questions = [ #Estos preguntas nos ayuda a recuperar la contraseña de las cuentas de los usuarios cuando quieren cambiar la conraseña 
    "What is your favorite color?",
    "What is your favorite animal?",
    "What is your favorite food?",
    "What is your favorite movie?",
    "What is your favorite book?",
    "What is your favorite game?",
    "What is your favorite sport?",
    "What is your favorite TV show?",
    "What is your favorite music?",
    "What is your favorite song?"
]

GameQuestions = {  #Preguntas Para el juego

    "Artista": "What is the Artist's Name ?",
    "Año": "What year was the song released?",
    "Album": "What is the album's name?",
    "Cancion": "What is the song's name?"

}

#?---------------------Funciones de base de datos Mysql ---------------------------------------------
#----------------------------------------------------------------------------------------------------
def CreatConnection(): #Este funcion sirve para crear la coneccion con la base de datos
    connexion = mysql.connector.connect(host="localhost", user="root", passwd="", database="Users")
    return connexion
def CreatDataBase(): #Este funcion sirve para crear la base de datos
    connexion = mysql.connector.connect(host="localhost", user="root", passwd="")
    cursor=connexion.cursor()
    query="CREATE DATABASE IF NOT EXISTS `Users`;"
    cursor.execute(query)
    connexion.commit()
    connexion.close()
    return True
def CreateTableUser(): #Este funcion sirve para crear la tabla User de la base de datos
    connexion = CreatConnection()
    cursor=connexion.cursor()
    query="""CREATE TABLE IF NOT EXISTS `UserData` \
            (`id` int(11) NOT NULL AUTO_INCREMENT,\
            `name` varchar(255) NOT NULL, \
            `Lastname` varchar(255) NOT NULL,\
            `age` int(11) NOT NULL CHECK (`age` >= 18),\
            `password` varchar(255) NOT NULL,\
            `email` varchar(255) NOT NULL CHECK (`email` LIKE '%@%.%'),\
            `Datereg` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
            `Username` varchar(255) NOT NULL,\
            `Gender` varchar(255) NOT NULL CHECK (`Gender` = 'Male' OR `Gender` = 'Female'),\
            `Question` varchar(255) NOT NULL ,\
            `Answer` varchar(255) NOT NULL,\
            `profile_image_url` varchar(255) NOT NULL,\
            PRIMARY KEY (`id`)) ;"""
    cursor.execute(query)
    connexion.commit()
    connexion.close()
    return True
def create_playlist_table(): #Este funcion sirve para crear la tabla playlist de la base de datos
    connection = CreatConnection()
    cursor = connection.cursor()
    query = """CREATE TABLE IF NOT EXISTS `playlists` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT,
                `artist_name` VARCHAR(255),
                `album_cover` VARCHAR(255),
                `song_name` VARCHAR(255),
                `duration_minutos` DECIMAL(5,2) NOT NULL,
                `audio_url` TEXT,
                FOREIGN KEY (`user_id`) REFERENCES `UserData`(`id`)
            );"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    return True


CreatDataBase()
CreateTableUser()
create_playlist_table()

def ConsultarUser(Username,Password):  # Consulta la base de datos para ver si existe el usuario
    global user_id
    
    connexion = CreatConnection()
    cursor=connexion.cursor()
    query="SELECT * FROM `UserData` WHERE `username`=%s AND `password`=%s;"
    cursor.execute(query, (Username, Password))
    result=cursor.fetchall()
    
    
    print("Resultados de la consulta:", result)
    # aqui se guarda el user_id si se encuentra en los resultados
    if result:
        user_id = result[0][0]
        
    connexion.close()
    return result

def ConsultarEmail(Username,Email):  # Consulta la base de datos para ver si existe el usuario y pasa el email y el username
    connexion = CreatConnection()
    cursor=connexion.cursor()
    query="SELECT * FROM `UserData` WHERE `username`=%s AND `email`=%s;"
    cursor.execute(query, (Username, Email))
    result=cursor.fetchall()
    connexion.close()
    return result



def get_user_playlists(user_id):  # Consulta la base de datos para ver si existe el usuario y pasamos el user_id
    connection = CreatConnection()
    cursor = connection.cursor()
    query = "SELECT * FROM `playlists` WHERE `user_id` = %s;"
    cursor.execute(query, (user_id,))
    playlists = cursor.fetchall()
    connection.close()
    return playlists

#----------------------------------------La Applicacion-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------

app = Flask(__name__, static_url_path='/static')

audio_file = None
audio_url = None
song_name = None
album_cover = None
artist_name = None
UserProfile = "Anafael Beats"
ProfilePicture = "https://github.com/RVDveloper/Beta4ProyectoAnafaelBeats/blob/main/static/img/_6a41bc42-cd48-4cdd-a4b6-bc2df6fda280.jpg?raw=true"
GuessQuestionGame=""
audio_urlbd = None
duration_milisegundos = None
duration_minutos = None
selected_audio_url=""




#---------------------------------------Funciones de la API----------------------------------------------
#--------------------------------------------------------------------------------------------------------
def try_api_request(url, headers, params): #Este funcion sirve para las llamadas a la API que nos permite hacer llamada a diferents apis, solo debemos pasar el url, headers y params
    for api_key in headers['X-RapidAPI-Key']:
        try:
            headers['X-RapidAPI-Key'] = api_key
            response = requests.get(url, headers=headers, params=params)
            if response.ok:
                return response
        except Exception as e:
            print(f"Error with API key {api_key}: {e}")
    return None

def get_top_artists(time_period): #Funcion para obtener los artistas mas populares, y el recommended artist
    url = "https://genius-song-lyrics1.p.rapidapi.com/chart/artists/"
    querystring = {"time_period": time_period, "per_page": "8", "page": "1"}
    headers = {
        "X-RapidAPI-Key": Recomended_ARTIST,
        "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
    }

    response = try_api_request(url, headers, querystring)
    
    if response:
        json_data = response.json()
        if json_data and 'chart_items' in json_data:
            artists = []
            count = 0
            for item in json_data['chart_items']:
                if count >= 8:
                    break
                artist_name = item['item']['name']
                if 'Genius' in artist_name:
                    continue
                artist_image = item['item']['image_url']
                artists.append({'artist': artist_name, 'image': artist_image})
                count += 1
            print(artists)    
            return artists
    else:
        print("Error en la solicitud a la API Genius en get_top_artists.")
        return []



def get_recommended_albums(time_period): #Funcion para obtener los albums mas populares y el recommended
    url = "https://genius-song-lyrics1.p.rapidapi.com/chart/albums/"
    querystring = {"time_period": time_period, "per_page": "5", "page": "1"}
    headers = {
        "X-RapidAPI-Key": Recomended_ALBUM,
        "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
    }

    response = try_api_request(url, headers, querystring)
    
    if response:
        json_data = response.json()
        albums = []
        for item in json_data['chart_items'][:5]:
            album_data = {
                'cover_art_thumbnail_url': item['item']['cover_art_thumbnail_url'],
                'name': item['item']['name'],
                'artist': item['item']['artist']['name']
            }
            albums.append(album_data)
        return albums
    else:
        print("Error en la solicitud a la API Genius en get_recommended_albums.")
        return []

def get_recommended_songs(time_period): #Funcion para obtener las canciones mas populares y el recommended
    url = "https://genius-song-lyrics1.p.rapidapi.com/chart/songs/"
    querystring = {"time_period": time_period, "per_page": "9", "page": "1"}
    headers = {
        "X-RapidAPI-Key": Recomended_Songs,
        "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
    }

    response = try_api_request(url, headers, querystring)

    if response:
        json_data = response.json()
        songs = []
        for item in json_data['chart_items'][:9]:
            song_data = {
                'artist_names': item['item']['artist_names'],
                'title': item['item']['title'],
                'song_art_image_url': item['item']['song_art_image_url']
            }
            songs.append(song_data)
        return songs
    else:
        print("Error en la solicitud a la API Genius en get_recommended_songs.")
        return []



@app.route('/update_search_value', methods=['POST']) 
def update_search_value(): #Funcion para actualizar el valor de la busqueda y mostrar los resultados
    global audio_file, audio_url, song_name, album_cover, artist_name, user_id, audio_urlbd, duration_milisegundos, duration_minutos
    required_value = request.form.get('search_value')

    url = "https://spotify23.p.rapidapi.com/search/"
    querystring = {"q": required_value, "type": "tracks", "offset": "0", "limit": "10", "numberOfTopResults": "5"}
    headers = {
        "X-RapidAPI-Key": Search_songs,
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = try_api_request(url, headers, querystring)
    
    if response:
        json_data = response.json()
        if json_data and 'tracks' in json_data and 'items' in json_data['tracks'] and json_data['tracks']['items']:
            artist_name = json_data['tracks']['items'][0]['data']['artists']['items'][0]['profile']['name']
            album_cover = json_data['tracks']['items'][0]['data']['albumOfTrack']['coverArt']['sources'][0]['url']
            song_name = json_data['tracks']['items'][0]['data']['name']
            duration_milisegundos = json_data['tracks']['items'][0]['data']['duration']['totalMilliseconds']

            def milisegundos_a_minutos(duration_milisegundos):
                minutos = duration_milisegundos / (1000 * 60)
                return minutos

            duration_minutos = milisegundos_a_minutos(duration_milisegundos)

            audio_file = search_song_on_youtube(song_name)
            if audio_file:
                audio_url = f"/static/audio/{os.path.basename(audio_file)}"
            
    return redirect(url_for('welcome'))



def search_song_on_youtube(song_name): #Funcion para buscar la cancion en youtube y retornar el audio
    try:
        results = YoutubeSearch(song_name, max_results=1).to_dict()
        if results:
            youtube_link = f"https://www.youtube.com{results[0]['url_suffix']}"

            if youtube_link:
                audio_file = download_video(youtube_link)
                return audio_file
    except Exception as e:
        print("Error searching for song on YouTube:", e)
    return None

def download_video(youtube_link): #Funcion para descargar el video
    global audio_urlbd, user_id, artist_name, album_cover, song_name
    try:
        video_id_temp = youtube_link.split('&')[0]
        video_id = video_id_temp.split('=')[-1]
        url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"
        headers = {
            "X-RapidAPI-Key": download_Video,
            "X-RapidAPI-Host": "youtube-media-downloader.p.rapidapi.com"
        }
        querystring = {"videoId": video_id}

        response = try_api_request(url, headers, querystring)

        if response:
            data = response.json()
            if data and 'audios' in data and 'items' in data['audios'] and data['audios']['items']:
                audio_url = data['audios']['items'][0]['url']
                audio_urlbd = audio_url

                try:
                    save_playlist_to_database(user_id, artist_name, album_cover, song_name, duration_minutos)
                except Exception as e:
                    print("Error al guardar en la base de datos:", e)

                response = requests.get(audio_url)
                filename = os.path.join(app.root_path, 'static', 'audio', f"{song_name}.m4a")
                with open(filename, 'wb') as f:
                    f.write(response.content)
                return filename
            else:
                print("No se encontró un enlace de descarga de audio en la respuesta de la API.")
        else:
            print("Error al obtener el enlace de descarga del archivo de audio desde la API.")
        return None
    except Exception as e:
        print("Error al descargar el audio:", e)
        return None


#Este funcion sirve para guardar la playlist en la base de datos
def save_playlist_to_database(user_id, artist_name, album_cover, song_name, duration_minutos):
    global audio_urlbd

    if user_id:
        connection = CreatConnection()
        cursor = connection.cursor()
        query = "INSERT INTO `playlists` (`user_id`, `artist_name`, `album_cover`, `song_name`, `duration_minutos`, `audio_url`) VALUES (%s, %s, %s, %s, %s, %s);"
        data = (user_id, artist_name, album_cover, song_name, duration_minutos, audio_urlbd)
        cursor.execute(query, data)
        connection.commit()
        connection.close()











#?---------------------------------funciones y rutas Flask ----------------------------------------

@app.route("/")  # ruta principal 
def index():
    return render_template("Home.html")


#-------------------------------------------------Login-----------------------------------------------------
@app.route("/login" , methods=["get"]) #la ruta de login para iniciar la pagina de login
def login():
    return render_template("login.html")

@app.route("/Registerlogin", methods=["POST"]) #la ruta de login para obtener los datos de un uaurio y consultar la base de datos
def Registerlogin():
    global UserProfile, ProfilePicture
    message=""
    if request.method == "POST":
        username=request.form["Username"]
        password=request.form["password"]
        results=ConsultarUser(username,password)
        if len(results) ==0:
            message="Invalid username or password"
            return render_template("confirmationLogin.html", message=message)
        else:
            UserProfile = username
            ProfilePicture = results[0][11]
            
            return redirect(url_for('welcome'))


#-------------------------------------------------SignUp-----------------------------------------------------



@app.route("/signUp", methods=["get"]) #la ruta de signup para iniciar la pagina de signup
def signUp():
    Question=random.choice(Questions)
    return render_template("sign.html", Question=Question)

@app.route("/register", methods=["POST"]) #la ruta de signup para obtener los datos de un uaurio y registrarlo en la base de datos
def register():
    global ProfilePicture
    
    if request.method == "POST":
        name = request.form["Name"]
        lastname = request.form["Lastname"]
        age = request.form["age"]
        email = request.form["email"]
        username = request.form["Username"]
        gender = request.form["gender"]
        password = request.form["password"]
        question = request.form["Question"]
        answer = request.form["Answer"]
        profile_image_url = request.form.get('profile_image_url', 'https://github.com/RVDveloper/Anafael-Beats-V2/blob/main/static/img/_e1135106-ec32-445d-ad40-d9fb257f977e.jpg')
        connection = CreatConnection()
        cursor = connection.cursor()
        query = "INSERT INTO `UserData` (`name`, `Lastname`, `age`, `password`, `email`, `Username`, `Gender`, `Question`, `Answer`, `profile_image_url`) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(query, (name, lastname, age, password, email, username, gender, question, answer, profile_image_url))
        connection.commit()
        connection.close()
        
        ProfilePicture=profile_image_url

    return render_template("confirmationSignUp.html")
@app.route("/ConfirmationSignUp") #la ruta de signup para iniciar la pagina de mostrar el mensaje de confirmacion el sign up
def ConfirmationSignUp():
    return render_template("confirmationSignUp.html")


#-------------------------------------------------ForgetPassword-----------------------------------------------------
@app.route("/ForgotPassword") #Este ruta sirve para mostrar el formulario de recuperar la contraseña si el usuario olvida su contraseña
def ForgotPassword():
    return render_template("forgetPassword.html")



Answer="" #Esta variable sirve para guardar la respuesta de la base de datos



@app.route("/ConfirmationForgetPassword", methods=["POST"]) #Este ruta sirve para decidir si el usuario existe en la base de datos para decidir si el usuario puede cambiar su contraseña o non 
def ConfirmationForgetPassword():

    message=""
    if request.method=="POST":
        email=request.form["email"]
        Username=request.form["Username"]
        result=ConsultarEmail(Username,email)
        if len(result) == 0:
            message="This email or username is not correct"
            return render_template("confirmationForgetPasswordStep1.html", message=message)
        else:
            message="We hope you can answer this question"
            global Answer
            Answer=result[0][10]
            return render_template("confirmationForgetPasswordStep2.html", Question=result[0][9], message=message) #La pregunta es para que el usuario puede cambiar su contraseña

@app.route("/AnswerForgetPassword", methods=["POST"]) #Este ruta sirve para decidir si la respuesta es correcta o no
def AnswerForgetPassword():

    if request.method == "POST":
        answer_user = request.form["AnswerUser"]
        answer_correct = Answer
        if answer_user == answer_correct:
            return render_template("restarPassword.html", AnswerCorrect=answer_correct)
        else:
            
            return render_template("confirmationForgetPasswordStep1.html", message="You have entered the wrong answer")

@app.route("/restarPassword", methods=["POST"]) #Este ruta sirve para cambiar la contraseña si la respuesta es correcta
def restarPassword():
    if request.method=="POST":
        password=request.form["password"]
        AnswerCorrect=request.form["AnswerCorrect"]
        connection=CreatConnection()
        cursor = connection.cursor()
        query="UPDATE `UserData` SET `password`=%s WHERE `Answer`=%s;"
        cursor.execute(query, (password, AnswerCorrect))
        connection.commit()
        connection.close()
        message="Your password has been changed successfully"
        return render_template("PasswordChanged.html", message=message)   

#----------------------------------------------------Dashboard----------------------------------------------------
@app.route('/dashboard') #Este ruta sirve para mostrar el dashboard
def welcome():
    global audio_url, UserProfile, ProfilePicture
    
    time_period = random.choice(["day", "week", "month", "all_time"])
    artists = get_top_artists(time_period)
            
      
    
    
        
    
    return render_template('dashboard.html', audio_url=audio_url , song_name=song_name, album_cover=album_cover, artist_name=artist_name, UserProfile=UserProfile, ProfilePicture=ProfilePicture, artists=artists)
#----------------------------------------------------Tranding---------------------------------------------------------



@app.route('/trending') #Este ruta sirve para mostrar la pagina de trending
def trendingPage():
    global audio_url, UserProfile, ProfilePicture
    
    time_period = random.choice(["day", "week", "month", "all_time"])
    artists = get_top_artists(time_period)
                
    recommended_albums = get_recommended_albums(time_period) 
    
    
    recommended_songs = get_recommended_songs(time_period)    
    
    return render_template('tranding.html', audio_url=audio_url , song_name=song_name, album_cover=album_cover, artist_name=artist_name, UserProfile=UserProfile, ProfilePicture=ProfilePicture, artists=artists, recommended_songs=recommended_songs, recommended_albums=recommended_albums)

#----------------------------------------------------Update---------------------------------------------------------
        
@app.route("/Settings",methods=["Get"]) #Este ruta sirve para mostrar la pagina de settings para cambiar los datos del usuario
def Settings():
    return render_template("settings.html")

@app.route("/Update",methods=["POST"]) #Este ruta sirve para verificar si el usuario introduce los datos correctos
def VerifyUpdate():
    if request.method=="POST":
        OldName=request.form["Name"]
        OldLastname=request.form["Lastname"]
        OldEmail=request.form["email"]
        OldUsername=request.form["Username"]
        result=ConsultarEmail(OldUsername,OldEmail)
        if len(result) == 0:
            message="This email or username is not correct"
            return render_template("confirmationForgetPasswordStep1.html", message=message)
        else:
            
            return render_template("Update.html", OldName=OldName, OldLastname=OldLastname, OldEmail=OldEmail, OldUsername=OldUsername)

@app.route("/ConfirmationUpdate", methods=["POST"]) #Este ruta sirve para cambiar los datos del usuario si el usuario introduce los datos correctos
def ConfirmationUpdate():
    if request.method=="POST":
        NewName=request.form["newName"]
        OldName=request.form["OldName"]
        NewLastname=request.form["NewLastname"]
        OldLastname=request.form["OldLastname"]
        NewAge=request.form["NewAge"]
        NewEmail=request.form["NewEmail"]
        OldEmail=request.form["OldEmail"]
        NewUsername=request.form["NewUsername"]
        OldUsername=request.form["OldUsername"]
        NewPassword=request.form["NewPassword"]
        connection=CreatConnection()
        cursor = connection.cursor()
        query="UPDATE `UserData` SET `name`=%s, `Lastname`=%s, `age`=%s, `email`=%s, `Username`=%s, `password`=%s WHERE `email`=%s and `Username`=%s;"
        Values=(NewName, NewLastname, NewAge, NewEmail, NewUsername, NewPassword, OldEmail, OldUsername)
        cursor.execute(query, Values)
        connection.commit()
        connection.close()
        UserProfile = NewUsername
        message="Your data has been updated successfully"
        return render_template("ConfirmationUpdate.html", message=message , UserProfile=UserProfile)
       
        

    
#---------------------------------------------Profile---------------------------------------------

@app.route("/Profile", methods=["GET"])
def Profile():
    Connection=CreatConnection()
    cursor = Connection.cursor()
    query = "SELECT * FROM `UserData` WHERE `Username` = %s and `id` = %s;"
    cursor.execute(query, (UserProfile, user_id))
    Result = cursor.fetchall()
    Name=Result[0][1]
    Lastname=Result[0][2]
    Email=Result[0][5]
    Username=Result[0][7]
    Age=Result[0][3]
    JoinData=Result[0][6]
    Gender=Result[0][8]

    Connection.close()
    return render_template("Profile.html",Name=Name, Lastname=Lastname, Email=Email, JoinData=JoinData, Username=Username, Age=Age, Gender=Gender)

#---------------------------------------------Playlist---------------------------------------------
@app.route('/playlist')
def playlist():
    global UserProfile

    
    playlists = get_user_playlists(user_id)

    
    playlist_range = f"1/{len(playlists)}" 

   
    selected_song_name = "Nombre de la canción seleccionada"

    
    selected_audio_url = None
    
    if selected_audio_url == None:
        for playlist1 in playlists:
                selected_audio_url = playlist1[6]
                selected_song_name = playlist1[4]
                break
    elif selected_audio_url == None and playlist == []:
          selected_song_name = "Selecciona una Cancion"
          selected_audio_url = "https://www.youtube.com/watch?v=ofPk4ajRA8I"

    
    for playlist in playlists:
        if playlist[5] == selected_song_name:
            selected_audio_url = playlist[6]
            break

    print("Este es el valor de selected_audio_url en la función playlist:", selected_audio_url)

    return render_template('PlaylistPage.html', UserProfile=UserProfile, playlists=playlists, playlist_range=playlist_range, selected_song_name=selected_song_name, selected_audio_url=selected_audio_url)

@app.route('/update_selected_song', methods=['POST'])
def update_selected_song():
    global selected_song_name, selected_audio_url
    if request.method == 'POST':
        data = request.json
        selected_song_name = data.get('selected_song', '')
        selected_audio_url = data.get('selected_audio_url', '')
        print("este es el valor en la funcion update:", selected_audio_url)
        return jsonify({'message': 'Selected song updated successfully', 'selected_song': selected_song_name, 'selected_audio_url': selected_audio_url}), 200
    return jsonify({'error': 'Invalid request method'}), 405

#-----------------------------------------The Game con Pandas ------------------------------------------------



dataframe= pd.read_csv("recurso/datos_artistas.csv") # Leer el archivo CSV y convertirlo en un DataFrame de pandas




AnswerGame = ""
Puntos = 0
Preguntas_realizadas = 0


dataframe['Año de lanzamiento'] = dataframe['Año de lanzamiento'].astype(str) # Convertir el tipo de dato de la columna 'Año de lanzamiento' en 'string' para que acepte cadenas de texto

dataframe.to_csv("datos_artistas_actualizado.csv", index=False) # Guardar el DataFrame actualizado en el archivo CSV


def sacar_lista_artistas(dataframe): # Función para sacar la lista de artistas del dataframe
    
    return dataframe["Artista"].unique().tolist()

def sacar_artista(lista_artistas): # Función para sacar un artista aleatorio de la lista de artistas

    return random.choice(lista_artistas)

def sacar_lista_anos(artista): # Función para sacar la lista de años de lanzamiento del artista


    dataframe_artista = dataframe[dataframe["Artista"] == artista]
    return dataframe_artista["Año de lanzamiento"].unique().tolist()

def sacar_anio(lista_anos): # Función para sacar un año aleatorio de la lista de años

    return random.choice(lista_anos)

def sacar_album(artista, anio): # Función para sacar un album aleatorio del artista en el año

    dataframe_album = dataframe[(dataframe["Artista"] == artista) & (dataframe["Año de lanzamiento"] == anio)]
    return random.choice(dataframe_album["Álbum"].unique().tolist())

def sacar_cancion(artista, album): # Función para sacar una cancion aleatoria del artista en el album

    dataframe_cancion = dataframe[(dataframe["Artista"] == artista) & (dataframe["Álbum"] == album)]
    return random.choice(dataframe_cancion["Canción"].unique().tolist())

def sacar_url_artista(artista): # Función para sacar la URL del artista

    dataframe_artista = dataframe[dataframe["Artista"] == artista]
    return dataframe_artista["URL Artista"].unique().tolist()[0]

def sacar_url_cancion(artista, album, cancion): # Función para sacar la URL de la cancion

    dataframe_cancion = dataframe[(dataframe["Artista"] == artista) & (dataframe["Álbum"] == album) & (dataframe["Canción"] == cancion)]
    return dataframe_cancion["URL Canción"].unique().tolist()[0]

def datos(): #Función para sacar los datos de las artistas , canciones , albums y años de lanzamiento

    lista_artistas = sacar_lista_artistas(dataframe)

    artista = sacar_artista(lista_artistas)

    lista_anos = sacar_lista_anos(artista)

    anio = sacar_anio(lista_anos)

    album = sacar_album(artista, anio)

    cancion = sacar_cancion(artista, album)

    url_artista = sacar_url_artista(artista)

    url_cancion = sacar_url_cancion(artista, album, cancion)

    return artista, anio, album, cancion, url_artista, url_cancion

def sacar_datos(preguntas): # Función para sacar los datos de las preguntas y las respuestas del juego

    question = random.choice(list(preguntas.values()))
    listaDatos=datos()

    if question == "What is the Artist's Name ?":
        
        guess_text = "Guess the Artist's Name"
        AnswerGame = listaDatos[0]
        url_dato = listaDatos[4]
        
    elif question == "What year was the song released?":
        
        guess_text = "Guess the year the song was released"
        AnswerGame = listaDatos[1]
        url_dato = listaDatos[5]

    elif question == "What is the album's name?":
        
        guess_text = "Guess the album's name"
        AnswerGame = listaDatos[2]
        url_dato = listaDatos[5]

    elif question == "What is the song's name?":
        
        guess_text = "Guess the song's name"
        AnswerGame = listaDatos[3]
        url_dato = listaDatos[5]

    return question, AnswerGame, url_dato, guess_text

@app.route("/AboutGame") #Este ruta es una definicion del juego 
def AboutGame():
    return render_template("AboutGame.html")

@app.route("/game") #la ruta de game para iniciar la pagina de game, el limite de las preguntas es de 10
def game():
    global AnswerGame, Puntos, Preguntas_realizadas
    question, AnswerGame, url_dato, guess_text= sacar_datos(GameQuestions)
    if Preguntas_realizadas < 10: 
        return render_template("game.html", Question=question, UrlDato=url_dato, GuessText=guess_text, Puntos=Puntos)
    else:
       
        Preguntas_realizadas = 0
        message = f"End of Game. Your final score is {Puntos} points."
        Puntos = 0
        return render_template("EndGame.html",message=message)

@app.route("/guess", methods=["POST"]) #La ruta deonde el usuario va ingresar las respuestas
def guess():
    global Puntos, Preguntas_realizadas
    guess = request.form["guessInput"].lower()
    Preguntas_realizadas += 1
    if guess == AnswerGame.lower():
        Puntos += 1
        message = f"Correct 😃! The answer was {AnswerGame}. Your current score is {Puntos} points."
        return render_template("ResultGame.html", Puntos=Puntos, message=message) 
    else:
        message = f"Incorrect 😔! The answer was {AnswerGame}. Your current score remains {Puntos} points."
        return render_template("ResultGame.html", AnswerGame=AnswerGame, Puntos=Puntos, message=message)


#----------------------------lyrics------------------------------------------
def get_lyrics(artist, song_title): #Este funcion es para hacer la llamada a la API de lyrics
    url = f"https://api.lyrics.ovh/v1/{artist}/{song_title}"
    response = requests.get(url)  # Aquí estaba el error
    
    if response.status_code == 200:
        data = response.json()
        lyrics = data.get("lyrics", "Lyrics not found")
        return lyrics
    else:
        return "Error: Unable to fetch lyrics"
@app.route("/lyrics", methods=["get"] ) #la ruta de lyrics para iniciar la pagina de lyrics
def lyrics():
    return render_template("lyrics.html")

@app.route("/DatosLyrics", methods=["POST"]) #la ruta de lyrics para iniciar la pagina de lyrics
def DatosLyrics():
    if request.method == "POST":
        Artist = request.form["Artist"]
        Music = request.form["Music"]
        lyrics = get_lyrics(Artist, Music)
        return render_template("ResultadoLyrics.html", lyrics=lyrics , Artist=Artist, Music=Music)

#----------------------------aboutus----------------------------------
@app.route("/About")  #la ruta de aboutus para iniciar la pagina de aboutus
def About():
    return render_template("AboutUs.html") 

@app.errorhandler(404)
def internal_server_error(e):
    
    app.logger.error(f"Server Error: {e}, route: {request.url}")
    return render_template('Error404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    
    app.logger.error(f"Server Error: {e}, route: {request.url}")
    return render_template('Error.html'), 500

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=False)


