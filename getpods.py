#!/usr/bin/python3
#
# A script to download and organize podcasts using wget.

import feedparser, os, re, datetime, wget
from dateutil import parser as time_parser

url_file = 'url_file'
down_speed = '5M'
pod_directory = '/media/denali/Podcasts'
pattern = re.compile(r'(.*)(\.mp3)(.*)')
debug = False

def parse_links(feed):
    '''
    Wget all podcast episodes to Title folder of RSS feed
    '''
    if hasattr(feed.feed, 'title'):
        title = feed.feed.title.replace('/','')
    else:
        title = None
        print('No title')

    path = os.path.join(pod_directory, title)
    if not os.path.exists(path):
        os.makedirs(path)

    if title:
        print('\nDownloading files from %s\n' % title)
        for f in feed.entries:
            if hasattr(f, 'published'):
                dateRaw = time_parser.parse(f.published)
                dPub = dateRaw.strftime('%Y%m%d') 
            else:
                dPub = None

            if hasattr(f, 'title'):
                episodeTitle = f.title.replace('"', '').replace('/','')
            else:
                episodeTitle = None

            if dPub:
                filename = '%s - %s.mp3' % (dPub, episodeTitle)
            elif episodeTitle:
                filename = '%s.mp3' % episodeTitle
            else:
                filename = None
            print(filename)
                

            try:
                for l in f.links:
                    download_mp3(l.href, path, filename)
            except:
                print('Links not formatted properly')
                pass
        


def download_mp3(link, path, filename):
     comp = pattern.match(link)
     if comp:
         download_link = comp.group(1)+comp.group(2)

         if not os.path.exists(os.path.join(path, filename)):
            wget.download(download_link, os.path.join(path, filename))


def main():

    with open(os.path.join(pod_directory, 'pod.log'), mode = 'a') as file:
        file.write('Started at %s\n' % datetime.datetime.now())
    urls= []
    for line in open(os.path.join(pod_directory, url_file)):
        li=line.strip()
        if not li.startswith('#'):
            urls.append(li.rstrip('\n'))


    for u in urls:
        feed = feedparser.parse(u)
        parse_links(feed)

    with open(os.path.join(pod_directory, 'pod.log'), mode = 'a') as file:
        file.write('Finished at %s\n' % datetime.datetime.now())



if __name__ == "__main__":
    main()
