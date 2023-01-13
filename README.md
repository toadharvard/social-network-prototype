# Social network prototype

## Features

* OAuth2 ❤️
* Create, update, delete articles 🖼️
* React with 👍👎 reactions
* Easy to add new features with adopted for pet-project clean architecture 👨‍💻

## TODO

* Make reactions independent of articles
* Add endpoint to get all users who liked your post
* Add and confuge logger
* Add more unit-tests for 100% coverage

## Run

### Production

1. `make env`
2. `make up-prod`

### Development

1. `make env`
2. `make dev`
3. `make up-dev`
4. `make run`

Go to `http://localhost/docs` to see open api docs

## List of all make commands

* `make help`

## Email validation with hunter.io

* Add `EMAILHUNTER_API_KEY=YOUR_API_KEY` to your .env file to use email hunter validation
