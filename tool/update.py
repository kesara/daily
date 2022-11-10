from csv import reader
from datetime import date
from sys import argv

from requests import codes, get


def iab_minutes(date):
    year = date.year
    query_date = date.isoformat()
    url = f"https://www.iab.org/documents/minutes/minutes-{year}/iab-minutes-{date}/"
    result = get(url)
    minutes = None
    if result.status_code == codes.ok:
        minutes = url
    return minutes


def iesg_minutes(date):
    year = date.year
    query_date = date.isoformat()
    url = f"https://www6.ietf.org/iesg/minutes/{year}/minutes-{date}.txt"
    result = get(url)
    minutes = None
    if result.status_code == codes.ok:
        minutes = url
    return minutes


def id_updates(date):
    query_date = date.isoformat()
    url = "https://www.ietf.org/id/all_id.txt"
    result = get(url)
    records = []
    if result.status_code == codes.ok:
        content = result.content.decode("utf-8")
        _records = list(reader(content.splitlines(), delimiter="\t"))
        records = [
            record for record in _records if len(record) > 1 and record[1] == query_date
        ]
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
