# Movies ROI Dashboard

## Problem Statement

Big box office numbers sound exciting, but they don’t always mean a movie actually made money. A film can earn hundreds of millions at the worldwide box office and still be a financial flop if the budget was huge, while a small indie film can quietly become a massive sleeper hit. I wanted to move beyond headline grosses and look at movies the way an investor or producer might: in terms of return on investment (ROI).

The goal of this project is to scrape and clean movie financial data (2018–2025) from [The Numbers](https://www.the-numbers.com/) using Selenium, then use that data to explore how budgets, revenues, distributors, genres, and MPAA ratings interact. With the processed dataset, I built interactive Tableau dashboards to answer questions like:
1.	Which movies became true sleeper hits, and which high-budget titles turned into flops based on net profit and ROI?
2.	How does production budget relate to worldwide box office across different performance categories (sleeper hit / normal / flop)?
3.	How is revenue split between domestic and international markets, and does that split differ by genre?
4.	Which distributors consistently deliver strong ROI over the years?
5.	How do genres and MPAA ratings relate to profitability and worldwide revenue?

The project is meant to be both analytical and visual: the goal isn’t just to crunch numbers, but to give anyone an intuitive way to explore which kinds of movies actually make money and why.

## Findings and Observations from the [Dashboard](https://public.tableau.com/app/profile/farhan.tanvir1622/viz/MovieROIDashboard20182025/ROIBudgetOverview)
1. Most movies in 2018–2025 are made on relatively small budgets, and only a few mega-budget projects exist.
2. On average, family-friendly ratings (G / PG / PG-13) generate more worldwide revenue than R-rated movies.
3. Horror and Concert/Performance films are small but very profitable by ROI, while genres like Western tend to perform the worst in terms of return.
4. The highest worldwide box office movies are usually in the international-heavy region, not the domestic-heavy side.
5. Universal has the highest overall ROI in the dataset, clearly ahead of other distributors.
6. The market is dominated by Action and Drama output, while niche genres stay small but sometimes surprisingly profitable.
7. Studios concentrate their output in mainstream genres even though some niche genres can have strong ROI.


## Build From Sources 
1. Clone the repo
```bash
git clone https://github.com/farhanPro05/movie_roi_dashboard.git
```
2. Intialize and activate virtual environment
```
python -m venv .venv
source ./.venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run all the cells of scrapper.ipynb file.
5. You will get a file named `movies_roi.csv` containing all the required fields.
Alternatively, check my scraped data here: https://github.com/farhanPro05/movie_roi_dashboard/blob/main/movies_roi.csv
