#!/usr/bin/env python3
"""
11장 파일 구조 확인 스크립트
"""

ORIGINAL_FILE = '/Users/woogis/Workspace/repo/ai-instructions/book/vol-2-part-4-chapter-11.md'

def inspect_file():
    """파일 구조를 분석합니다."""
    
    print('=== 파일 구조 분석 ===\n')
    
    with open(ORIGINAL_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.splitlines()
    
    print(f'파일 크기: {len(content) / 1024:.1f} KB')
    print(f'총 줄 수: {len(lines)}\n')
    
    # 처음 50줄 출력
    print('=== 파일 시작 (처음 50줄) ===\n')
    for i, line in enumerate(lines[:50], 1):
        print(f'{i:3d}: {line}')
    
    print('\n' + '='*60 + '\n')
    
    # 모든 ## 헤더 찾기
    print('=== 모든 ## 헤더 ===\n')
    for i, line in enumerate(lines, 1):
        if line.startswith('##'):
            print(f'{i:4d}: {line}')
    
    print('\n' + '='*60 + '\n')
    
    # 섹션 검색
    print('=== 섹션 검색 ===\n')
    
    patterns = ['## 11.1', '## 11.2', '## 11.3', '# 11', '##11']
    for pattern in patterns:
        idx = content.find(pattern)
        print(f'"{pattern}" 위치: {idx}')

if __name__ == '__main__':
    inspect_file()
    