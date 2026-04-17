#!/usr/bin/env python3

import os
import json
from urllib.parse import urlparse
import requests
import shutil
from resize_image import resize_image
from dateutil.parser import parse as date_parse


class FunderProcessor:
    """
    A class to process and fetch funder information from a remote JSON feed.

    This class provides methods to fetch funder data from a specified URL, process each funder entry,
    and generate corresponding markdown files and images for each funder.

    Methods:
        fetch_funders(): Fetches the funder data from the remote JSON feed.
        process_funder(item): Processes a single funder entry and generates the markdown file and image.
    """

    @staticmethod
    def fetch_funders():
        response = requests.get("https://changelog.qgis.org/en/qgis/members/json/")
        data = json.loads(response.text)
        items = data["rss"]["channel"]["item"]
        for item in items:
            FunderProcessor.process_funder(item)

    @staticmethod
    def process_funder(item):
        link = item["member_url"]
        image_url = item["image_url"]
        title = item["title"]
        level = item["member_level"]
        country = item["member_country"]
        start_date = item["start_date"]
        end_date = item["end_date"]

        start_date = date_parse(start_date, fuzzy_with_tokens=True)[0]
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = date_parse(end_date, fuzzy_with_tokens=True)[0]
        end_date = end_date.strftime("%Y-%m-%d")

        path = urlparse(image_url).path
        image_ext = os.path.splitext(path)[1]
        name = os.path.basename(os.path.normpath(link))
        image_name = "%s.%s" % (name, image_ext)
        image_name = image_name.replace("..", ".")

        content = f"""---
level: "{level}"
title: "{title}"
logo: "{image_name}"
startDate: "{start_date}"
endDate: "{end_date}"
link: "{link}"
country: "{country}"
---
"""
        markdown_filename = f"content/funders/{name}.md"
        with open(markdown_filename, "w", encoding="utf=8") as f:
            f.write(content)
            print(f"Writing: {markdown_filename}")

        response = requests.get(image_url, stream=True)
        image_filename = f"content/funders/{image_name}"
        with open(image_filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            print(f"Writing: {image_filename}")
        del response
        try:
            if level.lower() in ["flagship", "large"]:
                resize_image(image_filename, max_height=150)
            else:
                resize_image(image_filename)
        except Exception as e:
            print(f"Error resizing image: {e}")


if __name__ == "__main__":
    FunderProcessor.fetch_funders()
