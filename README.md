# supybot-ALwiki

This is a supybot/limnoria plugin that retrieves URLs from the arch linux wiki.

To use make sure you have the packages from requirements.txt installed:

* Requests
* BeautifulSoup
* Supybot/Limnoria

Then copy the "ALwiki" directory to your bot's plugin directory and load the
plugin. You can do this by typing "botname: load ALwiki" in irc after
identifying as an Admin. ("help identify" for info)

Usage in irc with the command prefix "!":

    meskarune | !alw urxvt

      supybot | meskarune: Urxvt - https://wiki.archlinux.org/index.php/Urxvt
