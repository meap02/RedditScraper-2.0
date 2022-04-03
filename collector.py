#! python3
#To access the reddit API
import praw
import prawcore
#Access webpages through HTML
import requests
#Serch through the HTML structure of webpages
from bs4 import BeautifulSoup
#regular expressions for sorting gathered links and naming convention
import re
#date and time for file naming convention
from datetime import datetime
#To save past objects of unique collections
import pickle
#to compare images and check for duplicates
import hashlib
import os
import pathlib


'''
This will scan every subreddit that this user posted to and then scan the 1000
most recent submissions from that subreddit for any more of the user's posts
'''


def collectUser(user_string: str,
                grab_limit: int,
                load_history: bool,
                search_subs: bool,
                location: str,
                collection):
    try:
        user = user_exists(user_string)
    except praw.exceptions.MissingRequiredAttributeException and \
            AttributeError as e:
        print("The praw.ini file is invalid" + str(e))
        yield("The praw.ini file is invalid,"
              + "please configure the file and restart the application")
        return
    if user is not None:
        print("Collecting "
              + str(grab_limit)
              + " posts from redditor: "
              + user.name)
        yield ("Collecting "
               + str(grab_limit)
               + " posts from redditor: "
               + user.name)
        #out = io.StringIO("Collecting posts from " + user.name + "...")
        user_path = pathlib.PurePath(location)
        try:
            os.mkdir(user_path / "Redditors")
            print("Made " + user_path.name + "!")
        except FileExistsError:
            pass
        except Exception as e:
            print("\\Redditors creation error" + str(e))
        user_path = user_path / "Redditors" / user.name
    else:
        print("User \"" + user_string + "\" does not exist")
        yield("User \"" + user_string + "\" does not exist")
        return
    root = []
    for item in user.submissions.new(limit=grab_limit):
        root.append(item)
    if load_history and checkUserDir(user_path):
        print("Loaded previous history...")
        yield "Loaded previous history..."
        with open(os.path.join(user_path, ".uni.pickle"), "rb") as f:
            uni = pickle.load(f)
            uurls = uni[0]
            usubs = uni[1]
            upics = uni[2]
    else:
        print("Did not load previous history...")
        yield "Did not load previous history..."
        uurls = set()
        usubs = set()
        upics = set()
    #usubs.add(user.subreddit.display_name)
    i = 0
    while i < len(root):
        if usubs.isdisjoint({root[i].subreddit.display_name}) and search_subs:
            print("New subreddit \""
                  + root[i].subreddit.display_name
                  + "\" found, getting newest "
                  + str(grab_limit) + " posts...")
            yield ("New subreddit \""
                   + root[i].subreddit.display_name
                   + "\" found, getting newest "
                   + str(grab_limit) + " posts...")
            leaves = root[i].subreddit.new(limit=grab_limit)
            usubs.add(root[i].subreddit.display_name)
            for leaf in leaves:
                if leaf.author is not None:
                    if (leaf.author == user) and uurls.isdisjoint({leaf.url}):
                        print("The post "
                              + "https://www.reddit.com" + leaf.permalink
                              + " has been added from "
                              + "\"" + root[i].subreddit.display_name + "\"")
                        yield ("The post "
                               + "https://www.reddit.com" + leaf.permalink
                               + " has been added from "
                               + "\"" + root[i].subreddit.display_name + "\"")
                        uurls.add(leaf.url)
                        collection.append(leaf)
            print("Finished scanning " + root[i].subreddit.display_name)
            yield ("Finished scanning " + root[i].subreddit.display_name)
            del leaves
        if(uurls.isdisjoint({root[i].url})):
            print("The post "
                  + "https://www.reddit.com" + root[i].permalink
                  + " has been added")
            yield ("The post "
                   + "https://www.reddit.com" + root[i].permalink
                   + " has been added")
            collection.append(root[i])
            uurls.add(root[i].url)
        else:
            print("The post "
                  + "https://www.reddit.com" + root[i].permalink
                  + " is a duplicate")
            yield ("The post "
                   + "https://www.reddit.com" + root[i].permalink
                   + " is a duplicate")
        i += 1
    i = 0
    print("Scanning photos for duplicates...")
    yield "Scanning photos for duplicates..."
    total = len(collection)
    while i < len(collection):
        if(re.search("/i\.imgur\.com/|i\.redd\.it", collection[i].url)):
            try:
                with requests.\
                        get(collection[i].url, allow_redirects=True) as f:
                    hsh = hashlib.md5(f.content).hexdigest()
                    if hsh in upics:
                        print("Removing duplicate: " + "https://www.reddit.com"
                              + collection[i].permalink)
                        yield ("Removing duplicate: "
                               + "https://www.reddit.com"
                               + collection[i].permalink)
                        collection.remove(collection[i])
                    else:
                        upics.add(hsh)
                        i += 1
            except ConnectionError:
                print("The url " + collection[i].url + " is not reachable")
                yield ("The url " + collection[i].url + " is not reachable")
                collection.remove(collection[i])
        else:
            i += 1
    if total != 0:
        print(str((1 - len(collection)/total)*100)
              + "% of posts were duplicate photos")
        yield (str((1 - len(collection)/total)*100)
               + "% of posts were duplicate photos")
    print("All " + str(len(collection)) + " unique posts have been collected")
    yield ("All " + str(len(collection)) + " unique posts have been collected")
    checkUserDir(user_path)
    with open(os.path.join(user_path, "log.txt"), "a") as f:
        f.write(str(datetime.today())
                + "__" + str(len(collection))
                + "_" + str(len(usubs)) + "\n")
    if load_history:
        uni = [uurls, usubs, upics]
        with open(os.path.join(user_path, ".uni.pickle"), "wb") as f:
            pickle.dump(uni, f)
        del uni, uurls, usubs, upics
    else:
        del uurls, usubs, upics
    return


def save(item: praw.models.Submission,
         user_str: str,
         location_str: str):

    user = user_exists(user_str)
    location = pathlib.PurePath(location_str) / "Redditors"
    try:
        os.mkdir(location)
    except FileExistsError:
        pass
    location = location / user.name
    name = str(str(datetime.fromtimestamp(item.created_utc))[0:10]
               + "_" + deClutter(item.title))
    print("Saving " + name + "...")
    yield ("Saving " + name + "...")
    ############################ TEXT #################################
    if "https://www.reddit.com" + item.permalink == item.url:
        print("This is a text post, will implement later...")
        yield "This is a text post, will implement later..."
    ############################ .gifv LINKS #################################
    elif re.search("\.gifv", item.url):
        try:
            soup = BeautifulSoup(requests.get(item.url).text, 'html.parser')
            dlink = soup.find('meta',
                              property="og:video",
                              recursive=True)['content']
            #Location to store image
            open(location / "videos" / (name
                                        + re.search("\.[^.\\/]+$",
                                                    dlink).group()),
                 'wb').write(requests.get(dlink).content)
        except ConnectionError:
            print("The link at " + item.url + " was not resolvable")
            yield("The link at " + item.url + " was not resolvable")
        except TypeError as e:
            print("The video was not able to be found within "
                  + item.url + str(e))
#                  + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            yield("The video was not able to be found within "
                  + item.url + str(e))
#                  + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        except Exception as e:
            print("An unknown error has occured while processing "
                  + item.url + ": " + str(e))
            yield("An unknown error has occured while processing "
                  + item.url + ": " + str(e))
    ############################ IMAGES ###############################
    elif(re.search("i\.redd\.it|/i\.imgur\.com/", item.url)):
        try:
            with requests.get(item.url, allow_redirects=True) as f:
                #Location to store image
                open(location / "pictures" / (name + re.search("\.[^.\\/]+$",
                                                               item.url).
                                              group()), "wb").write(f.content)
        except ConnectionError:
            print(item.url + "was not resolvable")
            yield (item.url + "was not resolvable")
        except Exception as e:
            print("An unknown error has occured while processing "
                  + item.url + ": " + str(e))
            yield ("An unknown error has occured while processing "
                   + item.url + ": " + str(e))
    else:
        try:
            soup = BeautifulSoup(requests.get(item.url).text, 'html.parser')
            dlink = soup.find('meta',
                              property="og:video", recursive=True)['content']
            #Location to store image
            open(location / "videos" / (name
                                        + re.search("\.[^.\\/]+$",
                                                    dlink).group()),
                 'wb').write(requests.get(dlink).content)
        except ConnectionError:
            print("The link at " + item.url + " was not resolvable")
            yield("The link at " + item.url + " was not resolvable")

        except TypeError as e:
            print("The video was not able to be found within "
                  + item.url + str(e))
#                  + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            yield("The video was not able to be found within "
                  + item.url + str(e))
#                  + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        except Exception as e:
            print("An unknown error has occured while processing "
                  + item.url + ": " + str(e))
            yield("An unknown error has occured while processing "
                  + item.url + ": " + str(e))


def deClutter(text):
    pattern = re.compile(pattern="["
                         u"\U0001F600-\U0001F7F0"  # emoticons
                         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                         u"\U0001F680-\U0001F6FF"  # transport & map symbols
                         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                         u"\U0001F911-\U0001F9EF"
                         u"\u24C2-\u2764"
                         "?"
                         "/"
                         "\\"
                         ":"
                         "\""
                         "*"
                         "|"
                         ">"
                         "<"
                         "."
                         "]+", flags=re.UNICODE)
    text = pattern.sub(r'', text).strip()
    if len(text) > 100:
        return text[0:100]
    else:
        return text


def checkUserDir(user_path: os.PathLike):
    try:
        os.mkdir(user_path)
        print("Made " + user_path.name + "!")
    except FileExistsError:
        pass
    except Exception as e:
        print("\\user_path creation error" + str(e))
    try:
        os.mkdir(user_path / "pictures")
        print("Made \\pictures!")
    except FileExistsError:
        pass
    except Exception as e:
        print("\\pictures creation error" + str(e))
    try:
        os.mkdir(user_path / "videos")
        print("Made \\videos!")

    except FileExistsError:
        pass
    except Exception as e:
        print("\\videos creation error" + str(e))
    try:
        open(user_path / "log.txt", "x").close()
    except OSError:
        pass
    try:
        with open(user_path / ".uni.pickle", "xb") as f:
            pickle.dump([set(), set(), set()], f)
    except OSError:
        pass
    return True


def user_exists(name):
    try:
        user = praw.Reddit().redditor(name)
        user.id
    except prawcore.exceptions.NotFound as e:
        return None
        print(e)
    return user


if __name__ == "__main__":
    beep = []
    print("Running module as script...")
    for y in collectUser("Your_submissive_doll", 10, False, False,
                         "X:\Personal\Coding\Python\RedditScraper 2.0", beep):
        print(y)
