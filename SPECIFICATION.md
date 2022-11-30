# Backend Take Home Project

You are the developer in charge of making the API that performs CRUD operations on the 
contents of a video streaming service. 

This API will provide endpoints for adding new movies in the platform, querying
existing ones, adding new actors, querying them, and additional endpoints showing movies
that some actors have made together, and common actors that appear in the requested movies.

## API endpoints

### add new movies
```
POST /movies
{
    "title": string,
    "category": string,
    "cast": Array<string>
}

return
422 if the body is malformed
400 if movie's title already exists
400 if at least one of the actors in the cast is not registered
200 if correct

if the request is successful it should store the movie
```
### query all movies
```
GET /movies

return 
200
Array<{
    "title": string,
    "category": string,
    "cast": Array<string>
}> (list of movie titles)
```
### add new actor
```
POST /actors
{
    "name": string,
    "age": number,
    "gender": "male" | "female"
}

return
422 is the body is malformed
400 if the actor's name already exists
400 if the actor's gender is not "male" or "female"
200

if the request is succesful it should store the actor
```
### query all actors
```
GET /actors

return
200
Array<{
    "name": string,
    "age": number,
    "gender": "male" | "female"
} > (list of actors)
```
### get movies in which all the requested actors appear
```
GET /performances?actors=string,string,...

return
400 if at least one of the actors does not exist
400 if the 'actors' query parameter is not sent
200
Array<{
    "title": string,
    "category": string,
    "cast": Array<string>
}> (list of movies where all the actors in the query appear)
```
### get actors that appear in all the requested movies
```
GET /common_actors?movies=string,string,...

return
400 if at least one movie does not exist
400 if 'movies' query parameter does not exist
200
Array<{
    "name": string,
    "age": number,
    "gender": "male" | "female"
}> (list of actors that appear in all requested movies)
```

### Project requirements
- Create the API that exposes all the requested endpoints in the language/framework you are more
  comfortable with.
- Create a README.md explaining how to install and launch the server.
- Implement automatic testing
- There is no need to implement a persistance layer or a deployment pipeline, but it would be nice
  if you explain how would you do it in a production environment.
- Create the Frontend side using React. In order to make it simple, the user will be allowed to perform just the operations related to movies, create the pages required: 
  - add new movies (route: /addmovie).
  - get all movies (route: /movies).
  - get movies in which all the requested actors appear (route: /movies). 
  
### Helpful take-home project guidelines:
- This project will be used to evaluate your skills, and should be fully functional without any obvious missing pieces. 
  We will evaluate the project as if you were delivering it to a customer.
- The deadline to submit your completed project is 5 days from the date you received the project requirements.
- If you schedule your final interview after the 5-days deadline, make sure to submit your completed project and all 
  code to the private repository before the deadline. Everything that is submitted after the deadline will not be taken 
  into consideration.
