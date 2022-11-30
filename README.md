# TAKE HOME

This application is intended to organize a movie library with its associated
actors. You will be able to see a catalog of movies and actors and you will be
able to apply filters on them. You can also create new movies and actors

## Requirements to run

  - Docker
  - Docker compose

## Requirements to develop

  - Docker
  - Docker compose
  - python 3.10.0
  - requirements_dev installed in your venv
  - Flake8 enabled in your IDE

## Before run app the first time

### Configure environment variables

You have to configure the environment variables file according with the
environment where the app will be executed:

The file where the environment variables must be written is **.env** and it
must contain the following:

```
POSTGRES_DB=<Name for stage postgres>
POSTGRES_USER=<User for stage postgres>
POSTGRES_PASSWORD=<Password for stage postgres>
DJANGO_USER=<Username for django superuser>
DJANGO_PASSWORD=<Password for django superuser>
APP_HOST=<Django API host to bind>
APP_PORT=<Django API port to bind>
APP_ALLOWED_HOSTS=<Allowed host in API separated by ; 0.0.0.0;localhost>
APP_DEBUG=<Django API Debug mode. This is optional, default False>
REACT_APP_NODE_ENV=<Node environtment development | production>
REACT_APP_SERVER_PORT=<Node server port>
```

> **NOTE:**
>
> For production environments is recommended to create this file in the deploy
> pipeline in order to keep the sensitive data in secret

### Configure Environment

To configure the environment it as easy as run the next command:

```
$ ./scripts/bootstrap.sh
```

This build all container (development and tests) and apply migrations in the
database

> **NOTE: If you are developer**
>
> You have to create a django superuser to enter to django admin. You can do
> it running this command:
>
> ```
> $ docker-compose run --rm api python manage.py createsuperuser
> ```
>
> And filling the required data

## Run app

When all of the previous steps be configured, you are ready to run the app.
Only you have to run the following command:

```
$ docker-compose up
```

You can access to rest framework frontend from your browser to test the API.
The host will be defined in the variable of the .env file called APP_HOST and
the port is defined in the APP_PORT variable.

Remember that APP_HOST must be included in APP_ALLOWED_HOSTS

For example if you have configured:
  - APP_HOST=0.0.0.0
  - APP_PORT=8000

You can access to rest framework frontend in the url **0.0.0.0:8000**

## Access to frontend

When the front container is launched you can access to frontend using the
url provided by the node development server.

This url is showed in console as follow as the next snipped:

```
front_1  | You can now view front in the browser.
front_1  |
front_1  |   Local:            http://localhost:3000
front_1  |   On Your Network:  http://172.26.0.4:3000
```

The correct url is _On Your Network: http://172.26.0.4:3000_

## Project structure

this project have three principal components:

1. **Infraestructure:** Conformed by _docker-compose.yml_ file and the _docker_
   folder. This contains the necessary configuration to lauch three containers.
    - One for Django API
    - Another for Postgres
    - And another for the frontend
    - Ideally another nginx container should be created to server the frontend
      as statics files and to pipe the api requests
2. **Api:** This contains the code of the API developed in Django. All code of
   the API is inside _api_ folder
3. **Frontend:** The frontend code is developed in React and is in _front_
   directory

Finally the file _.env_ configure all components and synchronize the django and
frontend settings with the docker-compose configuration

## API documentation

> **NOTE:**
>
> There are twice endpoints implemented in order to API documentation:
>
>   - **/swagger** To view the implemented endpoints, request and responses
>     types and for interact with API
>   - **/redoc** Only for view the implemented endpoints, parameters types,
>     reponses, request examples, etc and download OpenApi specification
>

### Actors endpoints

The endpoints defined for actor are the following:

#### GET /actors

Gets a list with all actors in the database

**Codes Returned:**

  - 200 OK: List with all actors

**Body Returned:**

  ```json
    [
      {
        "name": "name1",
        "age": 20,
        "gender": "male"
      },
      {
        "name": "name2",
        "age": 20,
        "gender": "female"
      },
      ...
    ]
  ```

#### GET /actors/\<name\>

Gets the data of the actor whose name is passed as \<name\>

**Codes Returned:**

  - 200 OK: JSON with the actor data
  - 404 NOT FOUND: If no Actor exists in the database with this name

**Body Returned:**

  ```json
    {
      "name": "name1",
      "age": 20,
      "gender": "male"
    }
  ```

#### POST /actors

Create new actor with the data passed as payload

**Body Payload:**

  - name: str
  - age: int
  - gender: str ["male" | "female"]

##### example:

  ```json
    {
      "name": "name1",
      "age": 20,
      "gender": "male"
    }
  ```

**Codes Returned:**

  - 422 UNPROCESSABLE ENTITY: If the payload is malformed
  - 400 BAD REQUEST: If the actor's name already exists
  - 400 BAD REQUEST: If the actor's gender is not "male" or "female"
  - 200 OK: If the actor has been created

#### PATCH /actors/\<name\>

Update actor whose name is passed as \<name\>

**Body Payload:**

  - name: str
  - age: int
  - gender: str ["male" | "female"]

##### example:

  ```json
    {
      "name": "name1",
      "age": 20,
      "gender": "male"
    }
  ```

**Codes Returned:**

  - 422 UNPROCESSABLE ENTITY: If the payload is malformed
  - 404 NOT FOUND: If no Actor exists in the database with this name
  - 400 BAD REQUEST: If the actor's gender is not "male" or "female"
  - 200 OK: If the actor has been updated

#### DELETE /actors/\<name\>

Remove actor whose name is passed as \<name\>

**Codes Returned:**

  - 404 NOT FOUND: If no Actor exists in the database with this name
  - 204 NOT CONTENT: If the actor has been removed

### Movies endpoints

The endpoints defined for movie are the following:

#### GET /movies

Gets a list with all movies in the database

**Codes Returned:**

  - 200 OK: List with all movies

**Body Returned:**

  ```json
    [
      {
        "title": "title1",
        "category": "terror",
        "cast": [
          "Actor 1",
          "Actor 2",
          ...
        ]
      },
      {
        "title": "title2",
        "category": "intrigue",
        "cast": [
          "Actor 3",
          "Actor 4",
          ...
        ]
      },
      ...
    ]
  ```

#### GET /movies/\<title\>

Gets the data of the movie whose title is passed as \<title\>

**Codes Returned:**

  - 200 OK: JSON with the movie data
  - 404 NOT FOUND: If no Movie exists in the database with this title

**Body Returned:**

  ```json
    {
      "title": "title1",
      "category": "terror",
      "cast": [
        "Actor 1",
        "Actor 2",
        ...
      ]
    }
  ```

#### POST /movies

Create new movie with the data passed as payload

**Body Payload:**

  - title: str
  - category: int
  - cast: list of str

##### example:

  ```json
    {
      "title": "title1",
      "category": "terror",
      "cast": [
        "Actor 1",
        "Actor 2",
        ...
      ]
    }
  ```

**Codes Returned:**

  - 422 UNPROCESSABLE ENTITY: If the payload is malformed
  - 404 NOT FOUND: If no Movie exists in the database with this title
  - 400 BAD REQUEST: If at least one of the actors in the cast is not
                     registered
  - 200 OK: If the movie has been created

#### PATCH /movies/\<title\>

Update movie whose title is passed as \<title\>

**Body Payload:**

  - title: str
  - category: int
  - cast: list of str

##### example:

  ```json
    {
      "title": "title1",
      "category": "terror",
      "cast": [
        "Actor 1",
        "Actor 2",
        ...
      ]
    }
  ```

**Codes Returned:**

  - 422 UNPROCESSABLE ENTITY: If the payload is malformed
  - 400 BAD REQUEST: If the movie's title already exists
  - 400 BAD REQUEST: If at least one of the actors in the cast is not
                     registered
  - 200 OK: If the movie has been created

#### DELETE /movies/\<title\>

Remove movie whose title is passed as \<title\>

**Codes Returned:**

  - 404 NOT FOUND: If no Movie exists in the database with this title
  - 204 NOT CONTENT: If the movie has been removed

### Performances endpoints

Implement one endpoint to obtain the movies where all the actors passed by
query parameter have acted

#### GET /performances/?actors=\<actor name 1\>,\<actor name 2\>,...

**Codes Returned:**

  - 400 BAD REQUEST: If at least one of the actors does not exist
  - 400 BAD REQUEST: if the 'actors' query parameter is not sent
  - 200 OK: List with all movies where all of actors passed by query params act

**Body Returned:**

  ```json
    [
      {
        "title": "title1",
        "category": "terror",
        "cast": [
          "name 1",
          "name 2",
          ...
        ]
      },
      {
        "title": "title2",
        "category": "intrigue",
        "cast": [
          "name 1",
          "name 2",
          "name 3",
          ...
        ]
      },
      ...
    ]
  ```

### Commond Actors endpoints

Implement one endpoint to obtain the actors that appear in all requested
movies passed by query params

#### GET /common_actors/?movies=\<movie title 1\>,\<movie title 2\>,...

**Codes Returned:**

  - 400 BAD REQUEST: If at least one movie does not exist
  - 400 BAD REQUEST: If 'movies' query parameter does not exist
  - 200 OK: List with all actors that appear in all movies passed by
            query params

**Body Returned:**

  ```json
    [
      {
        "name": "name1",
        "age": 20,
        "gender": "male"
      },
      {
        "name": "name2",
        "age": 35,
        "gender": "femlae"
      }
      ...
    ]
  ```

## Run tests

To run test you only have to run the next command:

```
$ ./scripts/runtests.sh
```
This command launch an api test container with the requirements and
requirements dev installed. And run api tests and checks flake8.

It would be a very good idea to configure the coverage tests

## Deploy to production

This project can be deployed on premise or in cloud.

For production environment the most important is change the .env file with the
production configuration. This .env contain sensitive data and is good idea
create it in the deploy pipeline.

You can deploy this project in aws using its ECS service, to deploy in aws you
can use a service of CD/CI like circleci that is based in containers.

In circleci platform you can set the production/stage environment variables
keeping then confidentials. With this environment variables you can make the
.env file in the deploy pipeline and the data of this environment variable
always will be safe.

Circleci service is configured with a .circleci.yml and you can defined steps.
This steps can run test, build the frontend and deploy in aws. You can use orbs
that will make you easy the deploy in ECS

> **FRONTEND DEPLOYMENT:**
>
> In the deployment pipeline the frontend must be builded and convert in
> statics files using **npm run build**. This files can be stored in S3 for web
> and expose using cloudfront
>