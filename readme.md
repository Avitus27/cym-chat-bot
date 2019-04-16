# CYM Bot

### Requirements
- Docker only

### Build
With Docker tools installed, the CYM bot container can
be built locally with 

    docker build . -t cym-bot
    
This will build an image tagged `cym-bot` locally.

### Run
The image can be run locally with (routing port 5000 on 
localhost to 5000 on the container)

    docker run -p 5000:5000 -it cym-bot
    
The flask server will start and expose port `8080`.
We can test this is running with.

    curl 0.0.0.0:5000
    curl: (52) Empty reply from server
