import docclass
categories={'Tech':[],'Economy':[],'Politics':[],'Sport':[]}
classifier = docclass.Classifier(categories.keys())

import feedparser


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


categories['Tech'] = ['http://rss.chip.de/c/573/f/7439/index.rss',
           'http://feeds.feedburner.com/netzwelt',
           'http://rss1.t-online.de/c/11/53/06/84/11530684.xml',
           'http://www.computerbild.de/rssfeed_2261.xml?node=13',
           'http://www.heise.de/newsticker/heise-top-atom.xml']

categories['Economy'] = ['http://newsfeed.zeit.de/wirtschaft/index',
              'http://www.faz.net/rss/aktuell/wirtschaft']

categories['Politics'] = ['http://www.welt.de/politik/?service=Rss',
               'http://www.faz.net/rss/aktuell/politik'
                'http://www.spiegel.de/politik/index.rss']

categories['Sport'] = ['http://www.faz.net/rss/aktuell/sport'
            'http://www.spiegel.de/sport/index.rss']

test=["http://rss.golem.de/rss.php?r=sw&feed=RSS0.91",
          'http://newsfeed.zeit.de/politik/index',
          'http://www.welt.de/?service=Rss',
          'http://rss.sueddeutsche.de/rss/Politik'
          'http://rss.sueddeutsche.de/rss/Sport'
          'http://rss.sueddeutsche.de/rss/Wirtschaft'
           ]




for key,value in categories.iteritems():
    for feed in value:
        print feed
        f=feedparser.parse(feed)
        for e in f.entries:
            fulltext=stripHTML(e.title+' '+e.description)
            print key
            classifier.train(fulltext,key)

for feed in test:
    f=feedparser.parse(feed)
    for e in f.entries:
        fulltext=stripHTML(e.title+' '+e.description)
        print fulltext
        print classifier.classify(fulltext)