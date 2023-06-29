from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors



app=FastAPI()


@app.get("/estrenos_mes/{mes}")
def obtener_coincidencias(mes: str):
    df = pd.read_csv("movies_credits.csv")  
    coincidencias = 0
    for index, row in df.iterrows():
        release_month = row["release_month"]
        if release_month.lower() == mes.lower():
            coincidencias = coincidencias+1

    return f"{coincidencias} es la cantidad de películas estrenadas en el mes de {mes}"


@app.get("/estrenos_dia/{dia}")
def buscar_coincidencias_dia(dia:str):
    df = pd.read_csv("movies_credits.csv")  
    coincidencias = 0
    for index, row in df.iterrows():
        release_days = row["release_day"]
        if release_days.lower() == dia.lower():
            coincidencias = coincidencias+1
    return f"{coincidencias} es la cantidad de películas estrenadas en los días {dia}"


@app.get("/score/{titulo}")
def obtener_informacion_pelicula(titulo):
    df = pd.read_csv("movies_credits.csv")
    pelicula = df[df['title'].str.lower() == titulo.lower()].iloc[0]  
    
    titulo = pelicula['title']
    anio_estreno = pelicula['release_year']
    score = pelicula['popularity']
    
    return f"La película {titulo} fue estrenada en el año {anio_estreno} con un score/popularidad de {score}"

@app.get("/votos/{titulo}")
def obtener_votos_pelicula(titulo:str):
    df = pd.read_csv("movies_credits.csv")
    pelicula = df[df['title'].str.lower() == titulo.lower()].iloc[0]  
    
    votos = pelicula['vote_count']
    promedio = pelicula['vote_average']
    
    if votos >= 2000:
        return f"La película {titulo} fue estrenada en el año {pelicula['release_year']}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio}"
    else:
        return f"La película {titulo} no cumple con la condición de tener al menos 2000 valoraciones."  
 
 
       
@app.get("/actor/{actor}")        
def obtener_informacion_actor(actor):
    df= pd.read_csv("F:\HENRY\DATA SCIENCE\PI\PI 1\movies_credits.csv")
    actor = actor.lower()
    peliculas_participadas = df[df['names_cast'].str.lower().str.contains(actor, na=False)]
    cantidad_peliculas = len(peliculas_participadas)
    
    if cantidad_peliculas > 0:
        retorno_total = round(peliculas_participadas['return'].sum(),2)
        promedio_retorno = round(retorno_total / cantidad_peliculas,2)
        return f"El actor {actor.capitalize()} ha participado en {cantidad_peliculas} filmaciones. Ha conseguido un retorno total de {retorno_total} con un promedio de {promedio_retorno} por filmación."
    else:
        return f"No se encontraron filmaciones en las que el actor {actor.capitalize()} haya participado."


@app.get("/director/{director}")
def get_director(nombre_director):
    df = pd.read_csv("F:\HENRY\DATA SCIENCE\PI\PI 1\movies_credits.csv")
    nombre_director = nombre_director.lower()
    director_movies = df[df['name_crew'].str.lower().str.contains(nombre_director, na=False)]
    cantidad_peliculas = len(director_movies)
    
    if cantidad_peliculas > 0:
        retorno_total = round(director_movies['return'].sum(), 2)
        promedio_retorno = round(retorno_total / cantidad_peliculas, 2)
        
        informacion_peliculas = []
        for index, row in director_movies.iterrows():
            pelicula = {
                'nombre': row['title'],
                'fecha_lanzamiento': row['release_date'],
                'retorno_individual': row['return'],
                'costo': row['budget'],
                'ganancia': row['revenue']
            }
            informacion_peliculas.append(pelicula)
        
        resultado = {
            'nombre_director': nombre_director.capitalize(),
            'cantidad_peliculas': cantidad_peliculas,
            'retorno_total': retorno_total,
            'promedio_retorno': promedio_retorno,
            'peliculas': informacion_peliculas
        }
        
        return resultado
    else:
        return None


# RECOMENDACIONES


# Definir el modelo de datos para recibir la entrada del usuario
class RecommendationRequest(BaseModel):
    pelicula: str

# Cargar los datos de películas desde el DataFrame
movies_data = pd.read_csv(r"F:\HENRY\DATA SCIENCE\PI\PI 1\movies_credits.csv")

# Preprocesamiento de los títulos de las películas para la nube de palabras
def preprocess_titles(text):
    # Realiza el preprocesamiento deseado, como eliminar signos de puntuación, convertir a minúsculas, etc.
    return text.lower()

# Agregar la columna 'title_processed' al DataFrame
movies_data['title_processed'] = movies_data['title'].apply(preprocess_titles)

# Generar una nube de palabras con las palabras más frecuentes en los títulos de las películas
def generate_wordcloud():
    # Preprocesar los títulos de las películas
    titles_processed = movies_data['title_processed'].apply(preprocess_titles)

    # Crear una matriz TF-IDF para representar los títulos de las películas como vectores numéricos
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(titles_processed)

    # Entrenar el modelo de KNN
    nn_model = NearestNeighbors(metric='cosine', algorithm='brute')
    nn_model.fit(tfidf_matrix)

    return nn_model, tfidf_vectorizer

# Función de recomendación de películas similares
def recomendacion(pelicula, nn_model, tfidf_vectorizer):
    # Obtener el índice de la película dada en el DataFrame
    movie_indices = movies_data[movies_data['title'] == pelicula].index

    if len(movie_indices) == 0:
        return []

    movie_index = movie_indices[0]

    # Transformar el título de la película en un vector TF-IDF
    title_vector = tfidf_vectorizer.transform([preprocess_titles(pelicula)])

    # Encontrar las películas más similares utilizando KNN
    _, indices = nn_model.kneighbors(title_vector, n_neighbors=6)  # Obtener las 6 películas más similares

    # Obtener los títulos de las películas similares
    similar_movies = movies_data.loc[indices.flatten()[1:], 'title'].values.tolist()

    return similar_movies

# Entrenar el modelo antes de recibir las solicitudes
nn_model, tfidf_vectorizer = generate_wordcloud()

# Decorador para la ruta de recomendaciones
@app.get("/recomendaciones/{pelicula}")
def get_recomendaciones(pelicula: str):
    recomendaciones = recomendacion(pelicula, nn_model, tfidf_vectorizer)
    return {"recomendaciones": recomendaciones}

    
    
    
    