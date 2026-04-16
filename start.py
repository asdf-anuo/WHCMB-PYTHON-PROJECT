# -*- coding: utf-8 -*-
from eur import ProjectDataCrawler


def main():
    """主函数"""
    crawler = ProjectDataCrawler()
    crawler.run_crawler()


if __name__ == "__main__":
    main()