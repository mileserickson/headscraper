"""Scrape email headers to a CSV file."""

from __future__ import print_function

from mailbox import mbox
import csv
import sys


class HeadScraper(object):
    """Scrape the headers of messages from an mbox file."""

    def __init__(self, mbox_name, cols=["To", "From", "Subject", "Date"]):
        """Create a new HeadScraper."""
        self.cols = cols
        self.mbox = mbox(mbox_name)

    @property
    def headers(self):
        """Yield each message header as a dictionary."""
        for msg in self.mbox:
            yield {col: msg[col] for col in self.cols}

    def write_csv(self, csv_name):
        """Output message headers to a CSV file."""
        with open(csv_name, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.cols)
            writer.writeheader()
            for header in self.headers:
                writer.writerow(header)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python headscrape.py sample.mbox [sample.csv]")
    else:
        mbox_name = sys.argv[1]
        hs = HeadScraper(mbox_name)
        if len(sys.argv) > 2:
            csv_name = sys.argv[2]
        else:
            csv_name = "{}.csv".format(mbox_name)
        print("Writing {}...".format(csv_name))
        hs.write_csv(csv_name)

