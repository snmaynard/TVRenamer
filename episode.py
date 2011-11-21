import re
import urllib
import xml.dom.minidom
import exceptions
import os
import string

class ParserError(exceptions.Exception):
    def __init__(self):
        return

class LookupError(exceptions.Exception):
    def __init__(self):
        return

class Episode:
    def parse_filename(self, filename):
        """Parse a filename into show name, season number and episode number"""
        
        formats = [r"(?P<show_name>.*)\.S(?P<season_number>[0-9]{2})E(?P<episode_number>[0-9]{2}).*\.(?P<file_extension>[a-zA-Z0-9]+)$",
                   r"(?P<show_name>.*)\.(?P<season_number>[0-9])(?P<episode_number>[0-9]{2}).*\.(?P<file_extension>[a-zA-Z0-9]+)$"
                  ]
  
        matched = False      
  
        for format in formats:
            p = re.compile(format, re.IGNORECASE)
            m = p.match(filename)
    
            if m:
                self.show_name      = m.group('show_name').replace(".", " ").replace("_", " ").strip().title()
                self.season_number  = m.group('season_number')
                self.episode_number = m.group('episode_number')
                self.file_extension = m.group('file_extension')
                
                matched = True
                break
        
        if matched == False:
            raise ParserError

    def get_episode_name(self):
        """Lookup the episode name on thetvdb.com"""
        
        # Get the TheTVDB show id
        url = "http://thetvdb.com/api/GetSeries.php?" \
              + urllib.urlencode({"seriesname" : self.show_name})

        print "Looking up Series: " + url

        handle = urllib.urlopen(url)
        dom = xml.dom.minidom.parse(handle)
        handle.close()
        
        shows = dom.getElementsByTagName("id")
        if shows.length:
            show_id = shows[0].childNodes[0].nodeValue
            if int(show_id) == 181771:
                show_id = "73244"
            if int(show_id) == 118511:
                show_id = "73244"
	    if int(show_id) == 77470:
                show_id = "73244"
        else:
            raise LookupError
        
        # Get episode details
        url = "http://thetvdb.com/api/CBBF66A9FDFECD1D/series/" \
              + show_id \
              + "/default/" \
              + self.season_number.lstrip("0") \
              + "/" \
              + self.episode_number.lstrip("0")

        print "Looking up episode: " + url
        handle = urllib.urlopen(url)
        dom = xml.dom.minidom.parse(handle)
        handle.close()
        
        episodes = dom.getElementsByTagName("EpisodeName")
        if episodes.length:
            self.episode_name = episodes[0].childNodes[0].nodeValue
        else:
            raise LookupError

    def create_file_path(self, format):
        """Create a new filename for the episode according to supplied format"""
        
        episode_number_short = str(int(self.episode_number))
        season_number_short = str(int(self.season_number))
        
        template = string.Template(format)
        replacements = {'show_name': self.show_name,
                        'season_number': self.season_number,
                        'season_number_short': season_number_short,
                        'episode_number': self.episode_number,
                        'episode_number_short': episode_number_short,
                        'episode_name': self.episode_name
                       }
                        
        return template.substitute(replacements) + "." + self.file_extension
