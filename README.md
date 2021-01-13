# moviesProject

App that will allow to search films based on given keyword.
OMDB API will be used.

SQLite DB file is within the code base.
It has two users created:

```admin:admin```


```test:admin12345```

The logged in user is able to search API using keyword and to add/remove films from his personalized 
Favorites List. 
## Prerequisites
1. Docker and docker-compose

## Usage
##### 1. Development instance, run command in ```docker-compose.yml``` directory:
```bash
docker-compose up movies
```
The app should be available on URL:
 ```http://127.0.0.1:8080```
## Execute tests
##### 1. Run tests in ```docker-compose.yml``` directory:
```bash
docker-compose up movies_tests
```
