#day32_db.py
#Neon PostgreSQL 에 입력과 처리 결과를 함께 저장하는 함수

import os
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb


# SQL 파일 경로
SQL_DIR = Path(__file__).resolve().parent / 'sql'


def execute(name: str, params: Any = ()):
    # 환경변수에서 데이터베이스 URL 획득
    url = os.getenv('DATABASE_URL', '').strip()

    if not url:
        raise ValueError(
            'DATABASE_URL environment variable not set'
        )

    sql = (SQL_DIR / name).read_text(encoding='utf-8')

    with psycopg.connect(
        url,
        connect_timeout=15,
        row_factory=dict_row
    ) as conn:
        # SQL 실행 후 결과를 리스트로 반환
        return conn.execute(sql, params).fetchall()


def save_run(title, result, request_key):
    title = title.strip()

    if not title or len(title) > 80:
        raise ValueError('기록 제목은 1~80자로 입력하세요')

    rows = execute(
        'save.sql',
        (
            title,
            result['title'],
            result['char_court'],
            result['word_court'],
            Jsonb(result['top_token']),
            result['version'],
            request_key
        )
    )

    return rows[0]['id']


# 리스트
def list_runs(keyword: str = ''):
    return execute(
        'list.sql',
        (f'%{keyword.strip()}%',)
    )


# 조회
def get_run(record_id):
    rows = execute('detail.sql', (record_id,))
    return rows[0] if rows else None


# 요약
def summary():
    return execute('summary.sql')[0]


# 삭제
def delete_run(record_id):
    return bool(execute('delete.sql', (record_id,)))















