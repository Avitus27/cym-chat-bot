# CYM Bot

### Requirements
- Docker only

### Configuration
This app takes a json configuration file `secret.json`
that has two values

`access_token`: Your Facebook Developers access token
for your page.

`verify_token`: The token you give Facebook to send
so you can verify that they are the the message sender

`secret.json`

    {
    "access_token": "YOUR_ACCESS_TOKEN",
    "verify_token" : "YOUR_VERIFY_TOKEN"
    }
### Build
With Docker tools installed, the CYM bot container can
be built locally with 

    docker build . -t cym-bot
    
This will build an image tagged `cym-bot` locally.

### Run
The image can be run locally with (routing port 5000 on 
localhost to 5000 on the container)

    docker run -p 5000:5000 -it cym-bot
    
The flask server will start and expose port `5000`.
We can test this is running with.

    curl 0.0.0.0:5000
    ok
