import sys
import os
import django
import feedparser
import html
from datetime import datetime
from django.utils.html import strip_tags

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_api_python.settings')

django.setup()

from articles.models import Publication, UserTag, Article
from django.db import connection

# rss_feeds = [ #uncomment these to initialize database, feel free to add or remove any
#     # --- Major Tech & Software Engineering ---
#     {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
#     {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml"},
#     {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index"},
#     {"name": "Wired", "url": "https://www.wired.com/feed/rss"},
#     {"name": "Engadget", "url": "https://www.engadget.com/rss.xml"},
#     {"name": "Gizmodo", "url": "https://gizmodo.com/rss"},
#     {"name": "Hacker News", "url": "https://hnrss.org/frontpage"},
#     {"name": "CNET", "url": "https://www.cnet.com/rss/news/"},
#     {"name": "ZDNET", "url": "https://www.zdnet.com/news/rss.xml"},
#     {"name": "Mashable", "url": "https://mashable.com/feeds/rss/all"},
#     {"name": "VentureBeat", "url": "https://feeds.feedburner.com/venturebeat/SZYF"},
#     {"name": "Smashing Magazine", "url": "https://www.smashingmagazine.com/feed/"},
#     {"name": "The New Stack", "url": "https://thenewstack.io/blog/feed/"},
#     
#     # --- Hardware, Maker & 3D Printing ---
#     {"name": "Hackaday", "url": "https://hackaday.com/blog/feed/"},
#     {"name": "Make: Magazine", "url": "https://makezine.com/feed/"},
#     {"name": "Arduino Blog", "url": "https://blog.arduino.cc/feed/"},
#     {"name": "Hackster.io", "url": "https://www.hackster.io/projects.rss"},
#     {"name": "All3DP", "url": "https://all3dp.com/feed/"},
#
#     # --- General Popular News ---
#     {"name": "BBC News", "url": "http://feeds.bbci.co.uk/news/world/rss.xml"},
#     {"name": "The New York Times", "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"},
#     {"name": "NPR", "url": "https://feeds.npr.org/1001/rss.xml"},
#     {"name": "CNN", "url": "http://rss.cnn.com/rss/cnn_topstories.rss"},
#     {"name": "The Washington Post", "url": "https://feeds.washingtonpost.com/rss/national"},
#     {"name": "The Guardian", "url": "https://www.theguardian.com/us/rss"},
#     {"name": "Wall Street Journal", "url": "https://feeds.a.dj.com/rss/RSSWorldNews.xml"},
#     {"name": "Associated Press", "url": "https://newsroom.ap.org/rss?query=TopicID:8910"},
#     {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
#     {"name": "Time", "url": "https://time.com/feed/"},
#     {"name": "CBS News", "url": "https://www.cbsnews.com/latest/rss/main"},
#     {"name": "Politico", "url": "https://rss.politico.com/politics-news.xml"},
#
#     # --- Motorsports & Automotive ---
#     {"name": "DirtFish", "url": "https://dirtfish.com/feed/"},
#     {"name": "Motorsport.com", "url": "https://www.motorsport.com/rss/"},
#     {"name": "Jalopnik", "url": "https://jalopnik.com/rss"},
#     {"name": "Top Gear", "url": "https://www.topgear.com/rss.xml"},
#
#     # --- Outdoors & Adventure ---
#     {"name": "Outside Online", "url": "https://www.outsideonline.com/feed/"},
#     {"name": "Expedition Portal", "url": "https://expeditionportal.com/feed/"},
#     {"name": "Field & Stream", "url": "https://www.fieldandstream.com/feed/"},
#     
#     # --- Software Engineering & Web Development ---
#     {"name": "FreeCodeCamp", "url": "https://www.freecodecamp.org/news/rss/"},
#     {"name": "DEV Community", "url": "https://dev.to/feed"},
#     {"name": "Real Python", "url": "https://realpython.com/atom.xml"},
#     {"name": "CSS-Tricks", "url": "https://css-tricks.com/feed/"},
#     {"name": "Stack Overflow Blog", "url": "https://stackoverflow.blog/feed/"},
#     {"name": "Martin Fowler", "url": "https://martinfowler.com/feed.atom"},
#     
#     # --- Electronics, Maker & Robotics ---
#     {"name": "IEEE Spectrum", "url": "https://spectrum.ieee.org/feeds/feed.rss"},
#     {"name": "Raspberry Pi", "url": "https://www.raspberrypi.com/news/feed/"},
#     {"name": "Adafruit Blog", "url": "https://blog.adafruit.com/feed/"},
#     {"name": "SparkFun", "url": "https://www.sparkfun.com/feeds/news"},
#     {"name": "HackSpace Magazine", "url": "https://hackspace.raspberrypi.com/feed"},
#
#     # --- Science & Space ---
#     {"name": "Space.com", "url": "https://www.space.com/feeds/all"},
#     {"name": "Science Daily", "url": "https://www.sciencedaily.com/rss/all.xml"},
#     {"name": "Nature", "url": "https://www.nature.com/nature.rss"},
#     {"name": "Scientific American", "url": "https://www.scientificamerican.com/rss/sparks.xml"},
#     {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/"},
#
#     # --- Gaming & Culture ---
#     {"name": "Polygon", "url": "https://www.polygon.com/rss/index.xml"},
#     {"name": "IGN", "url": "https://feeds.ign.com/ign/news"},
#     {"name": "Kotaku", "url": "https://kotaku.com/rss"},
#     {"name": "Game Informer", "url": "https://www.gameinformer.com/news.xml"},
#     
#     # --- Business & Finance ---
#     {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/news/rss"},
#     {"name": "The Economist", "url": "https://www.economist.com/the-world-this-week/rss.xml"},
#     {"name": "Harvard Business Review", "url": "https://feeds.hbr.org/harvardbusiness/"},
#     {"name": "Fortune", "url": "https://fortune.com/feed/"}
# ]
    

#for x in rss_feeds:        #uncomment this if copying repo and using for yourself to initialize database with publications
#    with connection.cursor() as cursor:
#        data_values = [x['name'], x['url']]
#        sql_string = "INSERT IGNORE INTO publication (name, publication_link, created_at) VALUES (%s, %s, CURRENT_TIMESTAMP)"
#        cursor.execute(sql_string, data_values)
#        new_publisher_id = cursor.lastrowid
#    publisher_feed = feedparser.parse(f"{x['url']}")

#with connection.cursor() as cursor:       #comment this while initializing publications, uncomment for scheduled regular rss feed scraping
#    cursor.execute("SELECT id, name, publication_link FROM publication")
#    rss_feeds = cursor.fetchall()

for x in rss_feeds:     #comment this while initializing publications, uncomment for scheduled regular rss feed scraping
    new_publisher_id = x[0]
    publisher_feed = feedparser.parse(f"{x[2]}")
    for entry in publisher_feed.entries:
        if not entry.get("tags", []):
            continue
        time_struct = entry.get("published_parsed") or entry.get("updated_parsed")
        if time_struct:
            clean_date = datetime(*time_struct[:6])
            db_ready_date = clean_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            continue
        with connection.cursor() as cursor:
            raw_summary = entry.get("summary", "")
            clean_summary = html.unescape(strip_tags(raw_summary))
            sql_string = "INSERT IGNORE INTO article (title, summary, link, published_at, publication_id, author, created_at) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)"
            
            data_values = [entry.get("title", ""), clean_summary, entry.get("link", ""), db_ready_date, new_publisher_id, entry.get("author", ""),]
            cursor.execute(sql_string, data_values)
            article_tags = entry.get("tags", [])
            new_article_id = cursor.lastrowid
            for tag in article_tags:
                get_string = "SELECT id FROM tag WHERE tag.name = %s"
                create_string = "INSERT IGNORE INTO tag (name, created_at) VALUES (%s, CURRENT_TIMESTAMP)"
                
                data_values = [tag.get("term", "").lower(),]
                cursor.execute(get_string, data_values)
                existing_tag = cursor.fetchone()
                if existing_tag == None:
                    cursor.execute(create_string, data_values)
                    new_tag_id = cursor.lastrowid
                else:
                    new_tag_id = existing_tag[0]
                junction_string = "INSERT IGNORE INTO article_tags (tag_id, article_id) VALUES (%s, %s)"
                junction_values = [new_tag_id, new_article_id]
                cursor.execute(junction_string, junction_values)
                