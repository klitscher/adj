# AmbientDJ (adj)

AmbientDJ is a tool for Dungeons and Dragons DMs to create a more immersive experience for their players. AmbientDJ allows DMs to create a playlist on the fly that fits the "mood" of whatever situation is currently happening: danger, battle, tavern, city, climax etc. AmbientDJ will then generate a playlist of the user's songs which match those "moods" and commence playing it. 

| Initial Setup | Main Screen |
| ------------- | ----------- |
| <img src="https://github.com/klitscher/adj/blob/master/docs/images/Initial_setup.png?raw=true" width="250" height="250"/> | <img src="https://github.com/klitscher/adj/blob/master/docs/images/main_view.png?raw=true" width="250" height="250"/> |

## Installation

Download the version that matches your operating system and extract the contents to a folder of your choice. 

## Usage

### Start AmbientDJ

Move into the adj_package folder which contains all the files. Then do the following depeding on you operating system: 

Linux
```
user$ ./adj.exe
```

Mac
```
Double click adj.exe
```

Windows
```
Double click adj.exe
```
### Use AmbientDJ

1. Follow prompt if this is your first time running AmbientDJ: This will tell AmbientDJ where to find your music files.
2. `Left click` on a mood to create a playlist of songs which have that mood and/or `Right click` on a mood to create a playlist of songs which DO NOT have that mood

| Include Mood | Exclude Mood |
| ------------ | ------------ |
| <img src="https://github.com/klitscher/adj/blob/master/docs/images/included.png?raw=true" width="250" height="250"/> | <img src="https://github.com/klitscher/adj/blob/master/docs/images/excluded.png?raw=true" width="250" height="250"/> |

3. Click `Activate` to start playing proposed playlist
4. Use `Play\Pause` and `Next Song` to control the music
5. Repeat steps `2 - 4` to generate a new playlist and overwite the current playlist

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## External Libraries

1. [BASS](http://www.un4seen.com/)
2. [Kivy](https://kivy.org/#home)

## Authors
[Sam Hermes](https://github.com/hermesboots)

[Kyle Litscher](https://github.com/klitscher)

[Rory Fahy](https://github.com/rmf10003)
