Propuesta de trabajo (requerimientos de aprobación):

Transformaciones:

Realizar las siguientes transformaciones en los datos:
Desanidar los campos como belongs_to_collection, production_companies y otros mencionados en el diccionario de datos para poder utilizarlos en consultas de la API.
Rellenar los valores nulos en los campos revenue y budget con 0.
Eliminar los valores nulos en el campo release date.
Asegurarse de que las fechas estén en formato AAAA-mm-dd y crear la columna release_year para extraer el año de la fecha de estreno.
Crear la columna de retorno de inversión llamada "return" calculada como revenue / budget, considerando 0 cuando no hay datos disponibles.
Eliminar las columnas no utilizadas: video, imdb_id, adult, original_title, poster_path y homepage.
Desarrollo de la API:

Proponer el uso del framework FastAPI para disponibilizar los datos de la empresa a través de la API.
Crear 6 funciones para los endpoints de la API con los siguientes decoradores: @app.get('/') para cada función.
Las funciones propuestas son:
cantidad_filmaciones_mes(Mes): Devuelve la cantidad de películas estrenadas en el mes consultado en el conjunto de datos.
cantidad_filmaciones_dia(Dia): Devuelve la cantidad de películas estrenadas en el día consultado en el conjunto de datos.
score_titulo(titulo_de_la_filmación): Devuelve el título, el año de estreno y el score/popularidad de una película según su título.
votos_titulo(titulo_de_la_filmación): Devuelve el título, la cantidad de votos y el valor promedio de votaciones de una película según su título. Si la película tiene menos de 2000 valoraciones, se muestra un mensaje indicando que no cumple con esa condición.
get_actor(nombre_actor): Devuelve el éxito medido en retorno, la cantidad de películas en las que ha participado y el promedio de retorno de un actor específico (excluyendo directores).
get_director(nombre_director): Devuelve el éxito medido en retorno, y la información de cada película (nombre, fecha de lanzamiento, retorno individual, costo y ganancia) en las que un director específico ha trabajado.
Deployment:

Utilizar servicios como Render, Railway u otros que permitan desplegar la API y hacerla accesible desde la web.
Análisis exploratorio de los datos (EDA):

Realizar un análisis exploratorio de los datos para investigar las relaciones entre las variables, identificar outliers o anomalías y descubrir patrones interesantes.
Utilizar herramientas como pandas profiling, missingno, sweetviz, autoviz, entre otras, para obtener conclusiones y visualizaciones relevantes, como nubes de palabras con las palabras más frecuentes en los títulos de las películas.
Sistema de recomendación:

Entrenar un modelo de machine learning para crear un sistema de recomendación de películas basado en la similitud de puntuación entre películas.
Ordenar las películas según su score de similitud y devolver una lista de Python con los 5 títulos de películas más similares, en orden descendente, dado un título de película de entrada.
Agregar esta función adicional llamada "recomendacion" a la API