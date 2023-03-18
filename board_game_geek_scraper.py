import requests
from bs4 import BeautifulSoup


def search_url(boardgame: str) -> str:
    return f"https://boardgamegeek.com/geeksearch.php?action=search&q={boardgame}&objecttype=boardgame"


def parse_game_icon_src(boardgame: str):
    url = search_url(boardgame)
    resp = requests.get(url)
    resp.raise_for_status()
    return parse_img_src(resp.content)


def parse_img_src(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")
    thumbnail_td = soup.find_all("td", class_="collection_thumbnail")[0]
    img = thumbnail_td.find_all("img")[0]
    return img.attrs["src"]


if __name__ == "__main__":
    import sys

    game_name = sys.argv[1].strip()
    img_src = parse_game_icon_src(game_name)
    print(img_src)
