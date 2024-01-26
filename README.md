# File MD5 provider with persistent Storage 


### It provides two endpoins 
1. /upload/ for file upload and provides ID for further access to result
2. /md5?task_id="<id_provided_by_fist_step>" provides info about task status and result  
3. There are simple front end interface to play with it  [http://localhost:8000](http://localhost:8000)

### Quick Start

Spin up the containers:

```sh
$ docker-compose up -d --build
```

Open your browser to [http://localhost:8000](http://localhost:8000)
