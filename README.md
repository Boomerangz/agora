# Agora

Python based hierarchical comment storage

### Install
Agora requires **PostreSQL** to be installed

To install you can execute:

```
git clone https://github.com/Boomerangz/agora.git
cd agora
pip3 install -r requirements.txt
python3 manage.py migrate
```

### Run

```
python3 manage.py runserver
```


### Configuration

All configs are stored in `agora/settings.py`
There you can change database hist, name, etc.

Also you can provide some environment variables for setup database and override credentials setted in config:
```
AGORA_DATABASE_HOST for database hostname
AGORA_DATABASE_NAME for database name
AGORA_DATABASE_USERNAME for database username
AGORA_DATABASE_PASSWORD for database username password
```

### Using
Agora provides simple REST API with just a few endpoints


##### To get comments list
**GET** ```http://localhost:8000/comments/```

You can also provide some GET parameters in url:

`parent_id` **AND** `parent_type` - to select children comments of some entity

`flat` (`0` or `1`) - to define if you want to receive full hierarchy of comments. It will be represented in flat list, children will follow parents, so you can re-create hierarchy from it

***
##### To post comment
**POST** ```http://localhost:8000/comments/``` with body like:
```
{
"text": "Some text",
"parent_id": 1,
"parent_type": "article",
"user": 1
}
```

You can provide any `parent_id` and any `parent_type`, but if you will provide `comment` as parent_type, the comment will be child of comment with ID you've provided.
Also you can provide any numeric user ID.
***
##### To get, update, delete single comment

**GET/PUT/PATCH/DELETE** ```http://localhost:8000/comments/<id>```
To update you have to provide with body like:
```
{
"text": "Some text",
"parent_id": 1,
"parent_type": "article",
"user": 1
}
```

You **CAN NOT DELETE** comments with existing children. Delete them first.
***
#### To get history of some comment changes
**GET** ```http://localhost:8000/comments/<id>/history```



#### To get comments of some user
**GET** ```http://localhost:8000/comments/user/<user_id>```


#### To download all comments in XML format
**GET** ```http://localhost:8000/comments/download/comments.xml```