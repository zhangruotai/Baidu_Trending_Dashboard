from __future__ import annotations

import re
import time

from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup

import pymysql
from backend.MySQL_Helper import MySQLHelper


@dataclass
class TrendingItem:
    rank: int
    title: str
    hot_index: int


class BaiduTrendingSpider:
    def __init__(self, db: MySQLHelper, timeout: int = 10):
        self.url = "https://top.baidu.com/board?tab=realtime"
        self.timeout = timeout
        self.db = db
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        }

    def fetch_page(self) -> str:
        response = requests.get(
            self.url,
            headers=self.headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.text

    def parse(self, html: str) -> List[TrendingItem]:
        soup = BeautifulSoup(html, "html.parser")
        items: List[TrendingItem] = []

        cards = soup.select(".category-wrap_iQLoo")

        for card in cards:
            rank_tag = card.select_one(".index_1Ew5p")
            title_tag = card.select_one(".c-single-text-ellipsis")
            hot_tag = card.select_one(".hot-index_1Bl1a")

            if not rank_tag or not title_tag or not hot_tag:
                continue

            rank_text = rank_tag.get_text(strip=True)
            title = title_tag.get_text(strip=True)
            hot_text = hot_tag.get_text(strip=True)

            if not rank_text.isdigit():
                continue

            hot_index = int(re.sub(r"\D", "", hot_text))

            items.append(
                TrendingItem(
                    rank=int(rank_text),
                    title=title,
                    hot_index=hot_index
                )
            )

        return items

    def create_table(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS baidu_trending (
            id INT PRIMARY KEY AUTO_INCREMENT,
            ranking INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            hot_index INT UNSIGNED NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4;
        """
        self.db.update(sql)

    def clear_table(self) -> None:
        sql = "TRUNCATE TABLE baidu_trending;"
        self.db.delete(sql)

    def save_to_mysql(self, items: List[TrendingItem]) -> None:
        sql = """
        INSERT INTO baidu_trending (ranking, title, hot_index)
        VALUES (%s, %s, %s)
        """

        for item in items:
            self.db.insert(sql, (item.rank, item.title, item.hot_index))

    def print_items(self, items: List[TrendingItem], limit: int = 20) -> None:
        print("Baidu Trending")

        for item in items[:limit]:
            print(
                f"排名: {item.rank} | "
                f"标题: {item.title} | "
                f"热搜指数: {item.hot_index}"
            )

    def run(self) -> List[TrendingItem]:
        start_time = time.time()

        html = self.fetch_page()
        items = self.parse(html)

        self.create_table()
        self.clear_table()
        self.save_to_mysql(items)
        self.print_items(items)

        end_time = time.time()

        print(f"\nTotal items fetched: {len(items)}")
        print(f"Time used: {end_time - start_time:.2f} seconds")
        print("Latest data saved to MySQL successfully.")

        return items


def ensure_database() -> None:
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="zzm123456"
    )

    with conn.cursor() as cursor:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS spider_db CHARACTER SET utf8mb4;"
        )

    conn.close()


if __name__ == "__main__":
    ensure_database()

    db = MySQLHelper(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="zzm123456",
        database="spider_db"
    )

    spider = BaiduTrendingSpider(db)
    spider.run()