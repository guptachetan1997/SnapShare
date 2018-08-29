# SnapShare

[RoundTable 2018 Project](https://docs.google.com/presentation/d/1VeNlU-PqQyFKN8m3Wo8ybEuWzkDZSNWLr21fOBu_Z6k/edit?usp=sharing)

Instagram clone with automatic image tagging.

<img src="https://github.com/guptachetan1997/SnapShare/blob/master/SnapShare.png" alt="alt text" width=200 height=200>

To run

```
$ redis-server
$ python3 server/src/manage.py runserver
$ python3 tagger/src/model_server.py
$ python3 tagger/src/model_process.py
```

To run via docker :
```
# go to the server directory
$ sudo docker build --file Dockerfile -t server .

# go to the tagger directory
$ sudo docker build --file Dockerfile-model_server -t tagger_server .
$ sudo docker build --file Dockerfile-model_process -t tagger_process .
$ 
$ sudo docker run -d -p 8000:8000 server
$ sudo docker run -d -p 5000:5000 tagger_server
$ sudo docker run -d tagger_process
$ sudo docker run -p 6379:6379 -d redis
```