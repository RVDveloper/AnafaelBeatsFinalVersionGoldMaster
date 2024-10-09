# Proyecto de Big Data: Aplicación Web de Música AnafaelBeats
**Developers**: RVDveloper & ANASSELMORABIT 

Profile: [ANASSELMORABIT](https://github.com/ANASSELMORABIT)  
Profile: [RVDveloper](https://github.com/RVDveloper)


![Anafael Logo](https://raw.githubusercontent.com/RVDveloper/Images/refs/heads/main/SCR-20241009-sibm.jpeg?raw=true)

## Descripción General

Este proyecto es una aplicación web de música similar a Spotify, construida utilizando Flask, MySQL, JavaScript y APIs. La aplicación permite a los usuarios explorar y reproducir música, crear listas de reproducción y obtener recomendaciones basadas en las Tendencias.

## Tecnologías Utilizadas

- **Flask**: Framework web en Python utilizado para desarrollar el backend de la aplicación, manejar la lógica del servidor y conectarse con las bases de datos.
- **JavaScript**: Lenguaje de programación utilizado para crear una interfaz de usuario interactiva y dinámica.
- **APIs**: Utilizadas para obtener datos de música, incluyendo información sobre canciones, artistas y álbumes.
- **MySQL**:  Utilizado para almacenar información de usuarios, canciones y listas de reproducción.

## Arquitectura del Proyecto

1. **Backend (Flask)**:
    - **API de Música**: Flask se utiliza para construir una API que gestiona solicitudes de datos de música. Utiliza bases de datos MySQL para almacenar información de usuarios, canciones y listas de reproducción.
    - **Autenticación y Autorización**: Manejo de autenticación de usuarios mediante Mysql para asegurar que solo los usuarios autorizados puedan acceder a ciertas funcionalidades.

2. **Frontend (JavaScript)**:
    - **Interfaz de Usuario (UI)**: Utiliza frameworks como bootstrap para construir una interfaz de usuario interactiva y responsive.
    - **Reproducción de Música**: Implementación de un reproductor de música que permite a los usuarios reproducir, pausar canciones.
    - **Listas de Reproducción**: Funcionalidad para crear, Reproducir listas de reproducción.

3. **APIs de Terceros**:
    - **API de Música**: Integración con servicios como Spotify API, genius-songs API & youtube-media API para obtener datos sobre canciones, artistas y álbumes.
    - **APIs de Recomendación**: Uso de APIs de recomendación musical para mejorar la precisión de las recomendaciones Genius-songs API.
    - **Api Busqueda de Lyrics**: Uso de API de Busqueda De Lyrics para el acceso a archivo con datos de millones de Lyrics la API lyrics.ovh.

## Funcionalidades Principales

- **Explorar Música**: Los usuarios pueden buscar y explorar canciones, álbumes y artistas.
- **Reproducción de Música**: Reproductor de música integrado que permite a los usuarios reproducir canciones directamente desde la aplicación web.
- **Listas de Reproducción**: Crear, Reproducir Listas de reproduccion de las canciones escuchadas por el usuario.
- **Recomendaciones de Tendencias**:  recomendación que sugieren música basada en la tendencia de canciones, albums, artistas que son tendencia mundial.
- **Perfil de Usuario**: Gestión de perfiles de usuario, incluyendo preferencias de música y listas de reproducción guardadas.
- **Juego Trivia**: Funcionalidad para jugar trivia musical.
- **Buscador de Lyrics**: Funcionalidad para buscar letras de canciones.

## Flujo de Trabajo

1. **Registro e Inicio de Sesión**: Los usuarios se registran y inician sesión en la aplicación.
2. **Exploración de Música**: Los usuarios buscan y exploran música utilizando la interfaz de usuario.
3. **Reproducción y Creación de PlayLists**: Los usuarios reproducen canciones y crean listas de reproducción basadas en su historial de escucha.
4. **Recomendaciones**: El sistema proporciona recomendaciones basadas en las tendencias mundiales.
5. **Gestión de Perfil**: Los usuarios pueden editar su perfil y gestionar sus listas de reproducción.
6. **Juego Trivia**: Los usuarios pueden participar en juegos de trivia musical.
7. **Búsqueda de Lyrics**: Los usuarios pueden buscar letras de canciones utilizando la API de lyrics.ovh.



