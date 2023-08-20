# lm-preference-human-eval

<img src="image/screenshot.png" />

## Setup
결과 저장용 MongoDB 띄우기 (docker)
```
docker run --name mongodb-humaneval -v ./data:/data/db -d -p 27017:27017 mongo
```