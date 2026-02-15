from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    base_url = "https://www.the-numbers.com"
    years = range(2018, 2026)
    contents = []

    for year in years:
        url = f"{base_url}/market/{year}/top-grossing-movies"
        print("Year page:", year, url)
        driver.get(url)
        time.sleep(1)

        tables = driver.find_elements(By.TAG_NAME, "table")
        table = tables[0]
        rows = table.find_elements(By.TAG_NAME, "tr")

        header_cells = rows[0].find_elements(By.TAG_NAME, "th")
        column_names = [th.text.replace("\n", " ").strip()
                        for th in header_cells]

        normalized_columns = []
        for name in column_names:
            if re.match(r"^\d{4}\s+Gross$", name):
                normalized_columns.append("Year Gross")
            else:
                normalized_columns.append(name)
        column_names = normalized_columns

        for row in rows[1:101]:
            tds = row.find_elements(By.TAG_NAME, "td")
            if not tds:
                continue

            row_dict = {}
            for idx, td in enumerate(tds):
                row_dict[column_names[idx]] = td.text.strip()

            a_tag = row.find_element(By.TAG_NAME, "a")
            href = a_tag.get_attribute("href")
            if not href.startswith("http"):
                href = base_url + href
            row_dict["Movie URL"] = href

            row_dict["Year"] = year

            print(row_dict)
            contents.append(row_dict)

    for row_dict in contents:
        movie_url = row_dict["Movie URL"]
        print("Movie:", movie_url)
        driver.get(movie_url)
        time.sleep(1)

        try:
            domestic_text = driver.find_element(
                By.XPATH,
                "//table[@id='movie_finances']//tr[.//b[contains(text(),'Domestic Box Office')]]/td[2]"
            ).text.strip()
            domestic_box = domestic_text
        except NoSuchElementException:
            domestic_box = None

        try:
            intl_text = driver.find_element(
                By.XPATH,
                "//table[@id='movie_finances']//tr[.//b[contains(text(),'International Box Office')]]/td[2]"
            ).text.strip()
            international_box = intl_text
        except NoSuchElementException:
            international_box = None

        try:
            world_text = driver.find_element(
                By.XPATH,
                "//table[@id='movie_finances']//tr[.//b[contains(text(),'Worldwide Box Office')]]/td[2]"
            ).text.strip()
            worldwide_box = world_text
        except NoSuchElementException:
            worldwide_box = None

        row_dict["Domestic Box Office"] = domestic_box
        row_dict["International Box Office"] = international_box
        row_dict["Worldwide Box Office"] = worldwide_box

        print(row_dict)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    for row_dict in contents:
        movie_url = row_dict["Movie URL"]
        print("Movie:", movie_url)
        movie_page = BeautifulSoup(requests.get(
            url=movie_url, headers=headers).text, "html.parser")

        production_cell = movie_page.find(
            string=lambda t: t and "Production" in t and "Budget" in t)
        if production_cell:
            production_cell_row = production_cell.find_parent("tr")
            tds = production_cell_row.find_all("td")
            production_budget = tds[-1].get_text(strip=True)
            production_budget = production_budget.split("(")[0].strip()
        else:
            production_budget = None

        mpaa_rating_cell = movie_page.find(
            "td", string=lambda t: t and "MPAA" in t and "Rating" in t)
        if mpaa_rating_cell:
            mpaa_rating_cell_row = mpaa_rating_cell.find_next_sibling("td")
            if mpaa_rating_cell_row:
                rating_a = mpaa_rating_cell_row.find("a")
            if rating_a:
                mpaa_rating = rating_a.get_text(strip=True)
        else:
            mpaa_rating = None

        row_dict["Production Budget"] = production_budget
        row_dict["MPAA Rating"] = mpaa_rating

        print(row_dict)

    df = pd.DataFrame(contents)
    df.to_csv("movies.csv", index=False)

    driver.close()
    return


if __name__ == "__main__":
    main()
