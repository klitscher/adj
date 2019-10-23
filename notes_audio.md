# Notes on the Atmospheric DJ Audio System

This document contains commentary on the Atmospheric DJ `audio` module the aspects of its design that are beyond the scope of normal documentation. By writing them down here, I hope I will not forget why I wrote things the way they are so that I do not break the parts that work.

## The `Music` Class

### Freeing Handles without Garbage Collection

Python's garbage collector does not have the ability to free the resources allocated by the low-level Bass library's functions. Since Python programmers are not going to expect manual resource management, I'd prefer to guarantee as strongly as possible that Bass resources are freed as soon as they are not needed.

The first step is to make sure that the `__del__` method frees the associated handle. This garbage collector is supposed to call this method just before destroying the object. This is simple enough on its own, but in the next section you will see that other precautions had to be taken with this method to avoid other side effects.

The Bass library provides a useful flag, `BASS_STREAM_AUTOFREE`, that is very thorough. It frees the resources associated with an audio channel whenever that channel stops (which is distinct from pausing). This includes when you call the "stop" function on the song, it ends naturally, or you tell it to fade out.

### Avoiding Reuse of Freed Handles

In practice, most Bass functions are idempotent for an audio channel. If you stop a channel while it is playing, it will stop playing. If you stop it again, even if the first "stop" caused Bass to free that channel, then the function will have no side effects.

In theory, there are only so many handles available for audio channels. I'm not sure how many handle values are available for Bass to use, and when it runs out it'd have to roll over and start using the first value again. Potentially, that means some code could hold a reference to a Python object with an old handle for a long enough time that its methods could influence a different song constructed much later.

The first part of fixing this involves using instance attributes to remember the state of the song so that the object doesn't always need to ask Bass. If you tell the song to stop, the object will remember that, which will prevent you from playing the song later.

The remaining situations are when the song ends as a result of something other than running a function that makes it do so. When the song ends naturally, Bass frees the handle even though you didn't direct it to. The class can track this event by using the callback function described more in the next section.

Finally, the song can stop unexpectedly when the sound device is unplugged, disabled, or some similar catastrophe happens at the operating system level. Currently, the class does not attempt to mitigate the variety of such failures.

### Minimizing Race Conditions

Bass decodes and plays sound in separate threads from the main one. This is desirable and causes no issues when all you care about is playing a single song and when you don't worry about what happens when it finishes. However, this is a program that generates playlists, so I need to write code that will recognize when a song ends.

Bass supports a limited set of callbacks on audio channels. One of them triggers when the channel reaches the end. (There is no callback for when the song ends as a result of a fade out, which may prove to be a problem later.)

By using callbacks, the main application now has to worry about triggering movement through a playlist outside the program's normal flow. For this purpose, Python's Global Interpreter Lock is a boon: code in two different methods can't interleave, avoiding situations where the playlist can try to skip the same song twice, layering the next song on top of itself.

However, calling two methods at the same time can still produce undesirable results. Even if calling the skip method twice won't double up on the music, it will still skip two songs forward when both threads of execution only intended to skip once. Fortunately, this is likely expected behavior for a user: if you click on the "skip" button just as the current song ends, you might guess that you clicked it slightly too late and accidentally skipped the next song just as it started.

The class's state tracking done with instance attributes, discussed above, should also mean that race conditions won't corrupt `Music` objects.