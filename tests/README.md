# Atmospheric DJ Unit Tests

## How to Run
Typically, with the source code installed in a directory called "adj" while you're in that directory's parent, you just run this command.

```python3
python3 -m unittest discover adj
```

## Manual Tests
Normally, when you run the test suite, all the tests run automatically and you're given a report of which pass and which fail. However, some tests require feedback from the tester and can't be run automatically. Running these tests requires extra steps.

To run the manual audio tests that ask you whether you can hear the music, set the environment variable `ADJ_DEVICE` to the index of your preferred sound device (to use the default one, set it to -1).

## Credits
The sample audio files come from [file-examples.com](https://file-examples.com/index.php/sample-audio-files/).
