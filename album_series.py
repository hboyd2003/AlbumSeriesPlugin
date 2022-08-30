# -*- coding: utf-8 -*-

# This is the Album Series plugin for MusicBrainz Picard.
# Copyright © 2022 Harrison Boyd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

PLUGIN_NAME = 'Album Series'
PLUGIN_AUTHOR = 'Harrison Boyd'
PLUGIN_LICENSE = 'GPL-2.0-or-later'
PLUGIN_LICENSE_URL = 'https://www.gnu.org/licenses/gpl-3.0.html'
PLUGIN_DESCRIPTION = '''Adds the tag series_name which contains the name of the series relation of a release'''
PLUGIN_VERSION = "0.5"
PLUGIN_API_VERSIONS = ["2.0"]


from picard.metadata import register_album_metadata_processor
from picard.webservice import WebService
from picard.webservice.api_helpers import MBAPIHelper
from picard import plugin

webservice = WebService()
mb_api = MBAPIHelper(webservice)

class Album_Series():
    def __init__(self, metadata, tagger, *args, **kwargs):
        self.metadata = metadata
        self.tagger = tagger
        
    def handler(self, document, http, error):
        if document['relations']:
            self.metadata['series_name'] = document['relations'][0]['series']['name']
            self.tagger.orig_metadata['series_name'] = document['relations'][0]['series']['name']
        self.tagger._requests -= 1
        self.tagger._finalize_loading(None)

def get_series(tagger, metadata, release):
    keeper = Album_Series(metadata, tagger)
    mb_api._get_by_id('release-group', metadata['musicbrainz_releasegroupid'], keeper.handler, ['series-rels'], priority=True, important=True)
    tagger._requests += 1


register_album_metadata_processor(get_series,priority=plugin.PluginPriority.HIGH)
