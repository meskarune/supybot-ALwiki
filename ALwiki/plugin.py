###
# Copyright (c) 2016, Dolores Portalatin
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

from supybot.commands import *
import supybot.callbacks as callbacks
import json
from urllib.parse import quote_plus
from requests import get
from requests.exceptions import RequestException

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('ALwiki')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class ALwiki(callbacks.Plugin):
    """Get information from the Arch Linux Wiki"""
    threaded = True

    def __opensearch(self, search):
        """Internal function to search using opensearch"""
        data = ""
        try:
            query = "https://wiki.archlinux.org/api.php?action=opensearch&search={0}&format=json".format(
                quote_plus(search))
            results = json.loads(get(query).text)
            description = results[1][0]
            link = results[3][0]
            if description:
                if len(description) > 250:
                    data = "{0}… - {1}".format(description[0:250], link)
                else:
                    data = "{0} - {1}".format(description, link)
            else:
                data = link
        except RequestException:
            return False

        return data

    def __querysearch(self, search):
        """Internal function to search using first query search to get the title of the page, then using opensearch"""
        data = ""
        title = ""
        try:
            query = "https://wiki.archlinux.org/api.php?action=query&list=search&srsearch={0}&format=json".format(
                quote_plus(search))
            results = json.loads(get(query).text)
            if "query" in results:
                if "searchinfo" in results:
                    if results["query"]["searchinfo"]["totalhits"] > 0:
                        title = results['query']['search'][0]['title']
            if title:
                data = self.__opensearch(title)
        except RequestException:
            return False

        return data

    def alw(self, irc, msg, args, search):
        """Search the arch linux wiki with alw <search>"""

        # Try first with opensearch
        data = self.__opensearch(search)

        # Then with query search
        if not data:
            data = self.__querysearch(search)

        irc.reply(data)
    alw = wrap(alw, ['text'])

Class = ALwiki

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
