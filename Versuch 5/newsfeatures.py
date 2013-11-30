# -*- coding: utf-8 -*-
import feedparser
import re
import pandas as pd
import csv

feedlist=['http://feeds.reuters.com/reuters/topNews',
          'http://feeds.reuters.com/reuters/businessNews',
          'http://feeds.reuters.com/reuters/worldNews',
          'http://feeds2.feedburner.com/time/world',
          'http://feeds2.feedburner.com/time/business',
          'http://feeds2.feedburner.com/time/politics',
          'http://rss.cnn.com/rss/edition.rss',
          'http://rss.cnn.com/rss/edition_world.rss',
          'http://newsrss.bbc.co.uk/rss/newsonline_world_edition/business/rss.xml',
          'http://newsrss.bbc.co.uk/rss/newsonline_world_edition/europe/rss.xml',
          'http://www.nytimes.com/services/xml/rss/nyt/World.xml',
          'http://www.nytimes.com/services/xml/rss/nyt/Economy.xml'
]

def stripHTML(h):
  p=''
  s=0
  for c in h:
    if c=='<': s=1
    elif c=='>':
      s=0
      p+=' '
    elif s==0:
      p+=c
  return p

from nltk.corpus import stopwords
sw = stopwords.words ('english')
def separatewords(text ):
    splitter = re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if len(s)>4 and s not in sw]

def getarticlewords():
    allwords = {}
    articlewords = []
    articletitles = []

    #Iterate over feeds
    for element in feedlist:
        f = feedparser.parse(element)
        f.feed.title

        #Iterate over articles
        for e in f.entries:
            #Add title to articletitles
            articletitles.append(e.title)

            fulltext=stripHTML(e.title+' '+e.description)
            seperatedFulltext = separatewords(fulltext)

            #Add words to allwords dictionary
            for word in seperatedFulltext:
                if word in allwords:
                    allwords[word] += 1
                else:
                    allwords[word] = 1

            #Add words to articlewords
            words = {}
            for word in seperatedFulltext:
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1
            articlewords.append(words)
    return allwords,articlewords,articletitles

def makematrix(allw, articlew):
    #Use only words that occur 4 or more times
    wordvec = dict((k, v) for k, v in allw.iteritems() if v >= 4)

    #Use only words that occur in less than 60% of all articles
    for word in wordvec:
        count = 0.0
        for article in articlew:
            if word in article.keys():
                count += 1
        if count/len(articlew) > 0.60:
            del wordvec[word]

    wordInArt= []
    for article in articlew:
        line = []
        for word in wordvec:
            if word in article.keys():
                line.append(article[word])
            else:
                line.append(0)
        wordInArt.append(line)
        
    return wordvec,wordInArt

allwords,articlewords,articletitles = getarticlewords()
wordvec,m = makematrix(allwords,articlewords)
df = pd.DataFrame(m, index=articletitles, columns=wordvec)
df.to_csv('test.csv', quoting=csv.QUOTE_NONNUMERIC)

print 'Zusammenfassung:\nArtikel: %d\nWörter gesamt: %d\nWörter gefiltert: %d' % (len(articletitles), len(allwords), len(wordvec))