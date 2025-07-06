[![Newest Release](https://img.shields.io/github/v/release/jordybronowicki37/stream-buddy?style=for-the-badge&logo=github&logoColor=fff&labelColor=555&color=94398d)](https://github.com/jordybronowicki37/stream-buddy/releases)
[![Newest Version](https://img.shields.io/github/v/tag/jordybronowicki37/stream-buddy?style=for-the-badge&logo=github&logoColor=fff&labelColor=555&color=94398d)](https://github.com/jordybronowicki37/stream-buddy/tags)
[![GitHub Profile](https://img.shields.io/static/v1.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=jordybronowicki37&message=GitHub&logo=github)](https://github.com/jordybronowicki37)
[![Docker image](https://img.shields.io/static/v1.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=Docker&message=latest&logo=docker)](https://github.com/jordybronowicki37/stream-buddy/pkgs/container/stream-buddy)
![Download count](https://img.shields.io/badge/Downloads-10%2B-94398d?style=for-the-badge)

```
███████╗████████╗██████╗ ███████╗ █████╗ ███╗   ███╗      ██████╗ ██╗   ██╗██████╗ ██████╗ ██╗   ██╗
██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗████╗ ████║      ██╔══██╗██║   ██║██╔══██╗██╔══██╗╚██╗ ██╔╝
███████╗   ██║   ██████╔╝█████╗  ███████║██╔████╔██║█████╗██████╔╝██║   ██║██║  ██║██║  ██║ ╚████╔╝
╚════██║   ██║   ██╔══██╗██╔══╝  ██╔══██║██║╚██╔╝██║╚════╝██╔══██╗██║   ██║██║  ██║██║  ██║  ╚██╔╝
███████║   ██║   ██║  ██║███████╗██║  ██║██║ ╚═╝ ██║      ██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝
```

Are you tired of not properly being notified by your favorite streamer starting their stream? \
Stream-buddy can help you with that! \
Stream-buddy keeps track of the status of your most favorite streamers and notify you.

# Features
- Automatically detect when a streamer goes online.
- Send streamer status messages to a discord channel.
- Provide a list of streamers from whatever site you want.
- Manually have control of the online detection mechanism by using html selectors.
- Easily host it yourself.

# Planned features
- Make it a full-fledged Discord bot with commands like:
  - Add streamer.
  - Remove streamer.
  - See who is online.
  - See all followed streamers.
- See the stream history of a streamer.
- Predict the stream schedule of a streamer by using their history.
- Automatically record a stream so that you can watch it back when you are busy.
- Handle multiple people using the bot independently and keep their followed streamers separate.

# Deployment
First you must have a `/data` folder in which the app can read and write all it's data. In this folder you initially 
need to provide the `setup.json` file. Use the `example-setup.json` file as a template.

## With Docker compose
With the [docker-compose.yml](./docker-compose.yml) file locally available. \
Create a `.env` file in the same directory as the `docker-compose` file and set the `DISCORD_WEBHOOK_URL` value. \
Alternatively you can modify the `docker-compose` file and set the environment variable manually. \

Then create the compose stack:
```shell
sudo docker compose up -d
```

To run the development compose stack:
```shell
sudo docker compose -f docker-compose-dev.yml up -d
```

## With Docker run
Change `YOUR_WEBHOOK_URL` with the webhook that you created in Discord. \
Also you can change `./data` to the actual path of your setup file on your host machine.

Create the container:
```shell
sudo docker run --name stream-buddy -e DISCORD_WEBHOOK_URL=YOUR_WEBHOOK_URL -v ./data:/app/data -d $(docker pull -q ghcr.io/jordybronowicki37/stream-buddy:latest)
```

To develop the container:
```shell
sudo docker run --name stream-buddy -e DISCORD_WEBHOOK_URL=YOUR_WEBHOOK_URL -v ./data:/app/data -d $(docker build -q .)
```
