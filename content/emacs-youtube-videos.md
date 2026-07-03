Title: Controlling a YouTube video from emacs
Author: Vineet Naik
Date: 2026-07-04
Tags: emacs, youtube, linux
Category: emacs
Summary: How to control a YouTube video playing in the browser from emacs using keybindings (on Linux)
Status: published
SeoDescription: Control YouTube videos in the browser from Emacs using playerctl and Linux's MPRIS2 D-Bus interface — no youtube-dl or mpv required.
OgImage: images/ogimage-emacs-youtube-videos.webp

Last week I shipped a YouTube section looper in
[Captrice](https://www.captrice.io), the guitar practice app I'm
building. It's meant for learning songs by ear — you mark a section of
the video to loop, play/pause, rewind as well as adjust playback
speed. Besides being a looper, it's also a keyboard-driven controller
for the YouTube video player embedded in the app so that you can
operate it easily while playing guitar. Here's a short preview:

<video controls>
    <source src="videos/captrice-looper.webm" />
</video>

That's not what this post is about though. Building this functionality
in Captrice made me wonder if it'd be similarly possible to control a
YouTube video playing in a browser from inside emacs using
keybindings. I have a simple use case — I use
[org-roam](https://www.orgroam.com/) to take notes while learning. If
the learning material is a YouTube video, I split the screen with the
browser on one side and emacs on the other. The problem is that
pausing or rewinding the video involves switching to the browser
window, interacting with the player, and then switching back (and the
same steps in reverse to resume). On MacOS the media controls on the
touch bar come in handy for this use case. It's the one thing I've
genuinely miss since moving to Linux.

Now if you know emacs, you can bet someone must have managed to get
YouTube videos playing inside the editor. And sure enough, there are packages
that turn emacs into a media player. But getting them to play YouTube
videos requires additional dependencies (youtube-dl, mpv etc.)  that
I'd like to avoid if possible. I'm happy with the video playing in the
browser as long as it can be controlled from emacs.

Turns out, it's quite trivial to achieve this. Most modern browsers on
Linux implement the
[MPRIS2](https://specifications.freedesktop.org/mpris/latest/) D-Bus
Interface out of the box. MPRIS2 stands for <u>M</u>edia <u>P</u>layer
<u>R</u>emote <u>I</u>nterfacing <u>S</u>pecification 2.0. To put it
simply, it's a standard Linux D-Bus interface through which a process
can control an MPRIS-compatible media player running in another
process.

When a web browser plays media, it registers itself as an MPRIS2
player on D-Bus and exposes its controls. The player can now be
controlled from another process by sending messages over D-Bus.
[playerctl](https://github.com/altdesktop/playerctl) is a command line
controller that makes this straightforward. For e.g. the following
command will pause the video in the browser (if it's playing) and resume (if it's
paused).

```bash
playerctl play-pause
```

Here's another handy command to rewind the video by 5 seconds

```bash
playerctl position 5-
```

There's however a
[bug](https://github.com/altdesktop/playerctl/issues/360) (actually in
YouTube's media player and not playerctl) that causes it to disregard
the offset and always seek (ahead or behind depending on the sign) by
5s. This means the following command will also seek behind by 5s
despite `15-` being specified as the offset

```bash
playerctl position 15-
```

Thankfully, the `position` command accepts an absolute position
(without the sign) too as input, so it's easy to work around this bug by
doing the calculation ourselves.

```bash
playerctl position $(echo $(playerctl position) | awk '{v=int($1)-15; print (v<0)?0:v}')
```

`playerctl position` without any further argument returns the current
position as a float. The awk command converts it to integer, subtracts
15 from it and clamps the result to 0 in case it's negative.

Coming back to emacs, all that's left to do now is to implement
interactive functions that shell-out to `playerctl` and define
keybindings for the same. We could also implement a MRPIS2 controller
in elisp but it seems like an overkill.

My emacs config looks something like this:

```elisp
(defun my/youtube-play-pause ()
  (interactive)
  (shell-command "playerctl play-pause"))

(defun my/youtube-rewind ()
  (interactive)
  (shell-command "playerctl pause && playerctl position $(echo $(playerctl position) | awk '{v=int($1)-15; print (v<0)?0:v}') && playerctl play"))

(define-prefix-command 'my/media-map)
(global-set-key (kbd "C-c m") 'my/media-map)
(define-key my/media-map (kbd "p") 'my/youtube-play-pause)
(define-key my/media-map (kbd "b") 'my/youtube-rewind)
```

Notice that the `playerctl position` command is wrapped in `pause && …
&& play`. I've observed that it works more reliably this way.

The `youtube-rewind` function can be parameterized to take the offset
as input. But I have kept it simple for now and may add support for
more control later if needed.

Here's a quick demo:

<video controls>
    <source src="videos/emacs-control-yt.webm" />
</video>

Due to the absence of audio, it's not immediately clear that the
YouTube video on the left is indeed playing in the beginning. But you
can follow the keybindings that appear in the right-bottom part of the
screen as I type them. Also notice that emacs is always the active
window for the entire duration which means I never switch to the
browser window.

And thus, it's so much easier to take notes while learning from a
video without interrupting the flow.
