# storeapi

Small Flask API for educational purposes.

## Description

A key-value store API server written in Python, with a MongoDB backend.

## Configuration

The API server is configured through environment variables.

| Environment Variable | Value               | Default Value             |
|----------------------|---------------------|---------------------------|
| MONGO_URI            | mongodb://IP:PORT   | mongodb://127.0.0.1:27017 |
| MONGO_DB             | Mongo Database Name | restdb                    |

## Installation
### Dependencies
* python3
* mongodb
* python3-pip (optional)
* virtualenv (optional)

### Deployment using virtualenv
```bash
$ virtualenv -p python3.8 venv/py38
$ source venv/py38/bin/activate
$ pip install -r requirements.txt
$ cd api
$ python -m flask run --host=0.0.0.0
```

## A sample installation done over an Ubuntu box
### DB

```bash
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

### APP
```bash
sudo apt install python3 python3-pip virtualenv git
git clone https://github.com/grobz/storeapi
cd storeapi
virtualenv -p python3.8 venv/py38
source venv/py38/bin/activate
pip install -r requirements.txt
cd api
python -m flask run --host=0.0.0.0

```

### Tests

```bash
curl --location --request POST 'http://127.0.0.1:5000/api/add' \
--header 'Content-Type: application/json' \
--data-raw '{
    "key":"TestKey",
    "data": {"Details":"Test Details","Attribute1":"Some attribute"}
}'

curl --location --request GET 'http://127.0.0.1:5000/api/get'
```

## Usage
This api has few methods to add / get / update information.

### /api/get
GET method to retrieve all keys in our database.
```bash
$ curl --location --request GET 'http://<IP>:<PORT>/api/get'
{
    "result": [
        {
            "data": {
                "KeyData1": 2,
                "KeyData2": 11,
                "KeyData3": 1,
                "KeyData4": "Avature"
            },
            "key": "Epsilon",
            "tags": {}
        },
        {
            "data": {
                "KeyData11": "Testing",
                "KeyData12": "Data",
                "KeyData13": "MoreData"
            },
            "key": "Delta",
            "tags": {}
        }
    ]
}
```

### /api/get/<key>
GET method to retrieve an specific key in our database.
```bash
$ curl --location --request GET 'http://<IP>:<PORT>/api/get/Epsilon'
{
    "result": {
        "data": {
            "KeyData1": 2,
            "KeyData2": 11,
            "KeyData3": 1,
            "KeyData4": "Avature"
        },
        "key": "Epsilon",
        "tags": {}
    }
}
```

### /api/add
POST method to add or replace a key.
```bash
$ curl --location --request POST 'http://<IP>:<PORT>/api/add' \
--header 'Content-Type: application/json' \
--data-raw '{
    "key":"Delta",
    "data": {"KeyData11":"Testing","KeyData12":"Data","KeyData13":"MoreData"}
}'
{
    "result": {
        "data": {
            "KeyData11": "Testing",
            "KeyData12": "Data",
            "KeyData13": "MoreData"
        },
        "key": "Delta",
        "tags": {}
    }
}
```

### /api/update
PUT method to merge in an existing key and create a new one if not.
```bash
$ curl --location --request PUT 'http://<IP>:<PORT>/api/update' \
--header 'Content-Type: application/json' \
--data-raw '{
    "key":"Delta",
    "data": {"KeyData11":"Overwrite Key","KeyData14":"NEW KEY Data"}
}'
{
    "result": {
        "data": {
            "KeyData11": "Overwrite Key",
            "KeyData12": "Data",
            "KeyData13": "MoreData",
            "KeyData14": "NEW KEY Data"
        },
        "key": "Delta",
        "tags": {}
    }
}
```
