from csv import reader
from datetime import date
from json import dumps
from sys import argv
from urllib.request import urlopen
from urllib.error import HTTPError


from bs4 import BeautifulSoup


MAILARCH = "https://mailarchive.ietf.org"


def iab_minutes(date):
    year = date.year
    url = f"https://www.iab.org/documents/minutes/minutes-{year}/iab-minutes-{date}/"
    minutes = None
    try:
        with urlopen(url):
            minutes = url
    except HTTPError:
        pass
    return minutes


def iesg_minutes(date):
    year = date.year
    url = f"https://www6.ietf.org/iesg/minutes/{year}/minutes-{date}.txt"
    minutes = None
    try:
        with urlopen(url):
            minutes = url
    except HTTPError:
        pass
    return minutes


def id_updates(date):
    url = "https://www.ietf.org/id/all_id.txt"
    records = []
    try:
        with urlopen(url) as f:
            content = f.read().decode("utf-8")
            _records = list(reader(content.splitlines(), delimiter="\t"))
            records = [
                {
                    'id': record[0],
                    'state': record[2]
                }
                for record in _records
                if len(record) > 1 and record[1] == str(date)
            ]
    except HTTPError:
        pass
    return records


def ietf_announce(date):
    url_date = date.strftime("%Y-%m")
    mailarchive_date = date.strftime("%b %d %Y")
    url = (
        f"{MAILARCH}/arch/browse/static/ietf-announce/{url_date}/"
    )
    records = []
    try:
        with urlopen(url) as f:
            soup = BeautifulSoup(f.read().decode("utf-8"), "html.parser")
            content = soup.find_all("ul", "static-index")[0].children
            capture = False
            for child in content:
                if child.name == "strong":
                    if capture:
                        break
                    capture = False
                    if mailarchive_date in child.text:
                        capture = True
                        continue
                if capture and child.name == "li":
                    link = child.find("a")
                    href = link.attrs["href"]
                    sender = child.find("em").text
                    records.append({
                        "link": f"{MAILARCH}{href}",
                        "title": link.text,
                        "sender": sender})
    except IndexError:
        pass
    except HTTPError:
        pass
    return records


if __name__ == "__main__":
    if len(argv) == 4:
        day = date(int(argv[1]), int(argv[2]), int(argv[3]))
    else:
        day = date.today()

    results = {
        "iab_minutes": iab_minutes(day),
        "iesg_minutes": iesg_minutes(day),
        "id_updates": id_updates(day),
        "ietf_announce": ietf_announce(day),
    }
    print(dumps(results))
