import urllib, time, os

import re

import sys


PREURL = r'http://music.baidu.com'

URL2 = r'http://music.baidu.com/artist'

URL3 = r'http://music.baidu.com/top'

FILE2 = r'all_artist.html'

FILE3 = r'all_song.html'

NL = '\n'


def grabpage(url,fileName):

        data = urllib.urlopen(url).read()

        coding = 'UTF-8'

        data = unicode(data, coding)

        f = open(fileName, 'w')

        f.write(data.encode(coding))

        f.close()


def matchData(filePath, resultFile, divType):
        fd = open(filePath, 'r')
        data = fd.read()
        data = unicode(data, 'UTF-8')
        if divType == 0:
                new_pattern = re.compile(u'title="[a-zA-Z\.]+[\sa-zA-Z\u4e00-\u9fa5]+"|title="[\u4e00-\u9fa5]+"',re.VERBOSE)
        elif divType == 1:
                new_pattern = re.compile(ur'\'\s?[title=\"]{7}[a-zA-Z0-9\s\u4e00-\u9fa5]+', re.VERBOSE)
        fin_all = re.findall(new_pattern, data)
        fin_all = list(set(fin_all))
        rst = ""
        for value in fin_all:
                rst += value.encode('UTF-8')
        # print rst
        del_pattern = re.compile('title="|"|\'', re.VERBOSE)
        rst = del_pattern.sub(" ",rst)
        # print rst
        nl_pattern = re.compile('\s{2,3}', re.VERBOSE)
        rst = nl_pattern.sub("\n", rst.strip())
        # print rst
        fd = open(resultFile, 'w')
        fd.write(rst)
        fd.close()


def singerDiv(filePath, divType):
        fd = open(filePath, 'r')
        data = fd.read()
        data = unicode(data, 'UTF-8')
        if divType == 0:
                p = re.compile(r'=?/?[artist]{6}/?[a-z]+/?[a-z]+', re.VERBOSE)
        elif divType == 1:
                p = re.compile(r'=?/?[style]{5}/?[A-Z0-9%]+|=?/?[tag]{3}/?[A-Z0-9%]+', re.VERBOSE)
                # p2 = re.compile(u'"?>?\s?[\u4e00-\u9fa5]{2,4}<?', re.VERBOSE)
        f = re.findall(p, data)
        # print f
        p1 = re.compile(r'/', re.VERBOSE)
        for url in f:
                url = PREURL + url
                tmp = p1.split(url)
                fname = tmp[-2] + tmp[-1] + '.html'
                result_file = tmp[-2] + tmp[-1] + '.txt'
                print 'URL: ' + url + NL + 'FILENAME: ' + fname + NL + 'RESULTFILE: ' + result_file + NL
                grabpage(url,fname)
                matchData(fname, result_file, divType)

def songDiv(filePath):
        fd = open(filePath, 'r')
        data = fd.read()
        data = unicode(data, 'UTF-8')
        p = re.compile(ur'top/[a-z]+">[\s0-9a-zA-Z\u4e00-\u9fa5]+<', re.VERBOSE)
        f = re.findall(p, data)
        rst = ""
        for value in f:
                rst += value.encode('UTF-8')
        rst = unicode(rst, 'UTF-8')
        p1 = re.compile(ur'">[\s0-9a-zA-Z\u4e00-\u9fa5]+<', re.VERBOSE)
        rst = p1.sub(" ", rst)
        url_list = rst.strip().split(' ')
        url_list = [value for value in url_list if value!='top/artist']
        for url in url_list:
                new_url = PREURL + '/' + url
                tmp = re.compile(r'/', re.VERBOSE).split(url)
                fname = tmp[-1] + '.html'
                result_file = tmp[-1] + '.txt'
                print 'URL: ' + new_url + NL + 'FILENAME: ' + fname + NL + 'RESULTFILE: ' + result_file + NL
                grabpage(new_url,fname)
                getSongName(fname, result_file)

def getSongName(filePath, resultFile):
        fd = open(filePath, 'r')
        data = fd.read()
        data = unicode(data, 'UTF-8')
        new_pattern = re.compile(u'song/[0-9a-zA-Z#]+\"\stitle=\"[0-9\s\'a-zA-Z\u4e00-\u9fa5\*&\u2019]+', re.VERBOSE)
        fin_all = re.findall(new_pattern, data)
        # print len(fin_all)
        rst = ""
        for value in fin_all:
                rst += value
        p = re.compile(u'song/[0-9a-zA-Z#]+\"\stitle=\"', re.VERBOSE)
        rst = p.sub("  ", rst)
        p1 = re.compile('\s{2}', re.VERBOSE)
        rst = p1.sub(NL, rst)
        rst = rst.strip().encode('UTF-8')
        # print rst
        fd = open(resultFile, 'w')
        fd.write(rst)
        fd.close()

if __name__ == '__main__':
        grabpage(URL3, FILE3)
        songDiv(FILE3)
        # getSongName('dayhot.html', '1.txt')
        # getSongName('dayhot.html', '1.txt')
        # singerDiv(FILE2, 0)
        # matchData('style%E4%B9%A1%E6%9D%91.html', '1.txt', 1)