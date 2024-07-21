from pathlib import Path

import psycopg2
from log import Logger


class Data():
    def __init__(self):
        # 保存日志的目录
        self.log_dir = Path('./log')
        self.log_dir.mkdir(exist_ok=True)

        # 日志, 保存时以时间命名
        self.logger = Logger(self.log_dir / 'data.log')

        self.conn = None
        self.cursor = None

        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                user='xxl',
                password='4444',
                host='198.19.249.83',
                port='5432',
                database='zhipin'
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            self.logger.error(f'connect error: {e}')

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
