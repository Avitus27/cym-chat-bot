start:
	docker build . -t cym-bot
	docker run --name cym-bot -p 5000:5000 -it cym-bot

restart:
	docker rm cym-bot
	docker build . -t cym-bot
	docker run --name cym-bot -p 5000:5000 -it cym-bot
