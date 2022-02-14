# DJI Release notes

This little project is meant to scrap DJI's release note page to check for update. It compares the website's version to what it has seen last time, and will output a notification.

## Run

```shell
$ ./check_dji_releases.sh
Nothing new! ✅
iOS: iOS Mobile SDK Release Note v4.15.2 2021-10-11 en
Android: Android Mobile SDK Release Note v4.16 2021-12-29 en
```


## Setup

You'll probably need to change some stuff to make it work for you, I've hard-coded some paths for example.

I use it with cron to run every weekday at 10:
```crontab
30 9 * * 1-5 bash -c "~/.bin/DJIReleaseNotes/check_dji_releases.sh"
```
