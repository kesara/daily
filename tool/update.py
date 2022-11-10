from csv import reader
from datetime import date
from sys import argv
from urllib.request import urlopen
from urllib.error import HTTPError


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
        with urlopen(url) as result:
            content = result.read().decode("utf-8")
            _records = list(reader(content.splitlines(), delimiter="\t"))
            records = [
                record
                for record in _records
                if len(record) > 1 and record[1] == str(date)
            ]
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
    }
    print(results)
