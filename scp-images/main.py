from bs4 import BeautifulSoup
import requests as rq

series_urls = [
    "https://scp-wiki.wikidot.com/scp-series",
    "https://scp-wiki.wikidot.com/scp-series-2",
    "https://scp-wiki.wikidot.com/scp-series-3",
    "https://scp-wiki.wikidot.com/scp-series-4",
    "https://scp-wiki.wikidot.com/scp-series-5",
    "https://scp-wiki.wikidot.com/scp-series-6",
    "https://scp-wiki.wikidot.com/scp-series-7",
    "https://scp-wiki.wikidot.com/scp-series-8"
]
base_url = "https://scp-wiki.wikidot.com"

from typing import Tuple, List

def get_all_links(url_list: List[str]) -> List[Tuple[str, str]]:
    scp_links = []
    for idx, url in enumerate(url_list):
        response = rq.get(url).content
        soup = BeautifulSoup(response, "html.parser")
        li_links = soup.select(".content-panel.standalone.series")[0].select("ul li")

        for li in li_links:
            a = li.select_one("a")
            if "/scp" in a.get("href"):
                scp_links.append((f"{base_url}{a.get('href')}", li.get_text()))
                
        print(f"Finished fetched series {idx+1}")
                
    return scp_links

all_scp_links = get_all_links(series_urls)

all_scp_links_clean = filter(lambda x: "SCP-" in x[1], all_scp_links)

all_scp_links_clean = list(all_scp_links_clean)

def get_image(url: str) -> str:
    r = rq.get(url).content
    s = BeautifulSoup(r, "html.parser")
    img = s.select_one(".scp-image-block.block-right")
    if img == None:
        return ""
    
    img_link = img.select_one("img")
    if img_link != None:
        return img_link.get("src")
    
    iframe_link = img.select_one("iframe").get("src")
    return f"{base_url}{iframe_link}"

all_scp_dict = []

for link, name in all_scp_links_clean:
    image_link = get_image(link)
    if image_link == "":
        print(f"Skipping {name}")
        continue
    
    all_scp_dict.append({
        "name": name,
        "image_link": image_link
    })
    
    print(f"Collected {name}")

import json

with open("scp-images.json", "w") as fp:
    json.dump(all_scp_dict, fp, indent=2)
