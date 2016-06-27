"""Scrape email headers to a CSV file."""

from __future__ import print_function

from mailbox import mbox
import csv
import sys


class HeadScraper(mbox):
    """Scrape the headers of messages from an mbox file."""

    def __init__(self, mbox_name, cols=["To", "From", "Subject", "Date"]):
        """Create a new HeadScraper."""
        self.cols = cols
        mbox.__init__(self, mbox_name)

    @property
    def headers(self):
        """Yield each message header as a dictionary."""
        for msg in self:
            header = {col: msg[col] for col in self.cols}
            yield header

    def write_csv(self, csv_name):
        """Output message headers to a CSV file."""
        with open(csv_name, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.cols)
            writer.writeheader()
            for header in self.headers:
                writer.writerow(header)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mbox_name = sys.argv[1]
        hs = HeadScraper(mbox_name)
        if len(sys.argv) > 2:
            csv_name = sys.argv[2]
        else:
            csv_name = mbox_name+".csv"
        print("Writing {}...".format(csv_name))
        hs.write_csv(csv_name)

    else:
        print("Usage: python headscrape.py sample.mbox [sample.csv]")
