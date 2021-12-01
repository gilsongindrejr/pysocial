# Pysocial

Social network backend using django 3. 

# Running the project

#### Clone this repository
```
$ git clone <https://github.com/gilsongindrejr/pysocial.git>
```

#### Access the project folder
```
$ cd Pysocial
```

#### Build the container
```
$ docker-compose up --build -d
```

#### Migrate the database
```
$ docker-compose exec web python manage.py migrate
```
#### Create super user
```
$ docker-compose exec web python manage.py createsuperuser
```

##### The server will be initiated on port 80 - access <http://127.0.0.1> 

# Server shell
```
$ docker-compose exec web bash
```
