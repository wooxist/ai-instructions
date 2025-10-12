#!/usr/bin/env python3
"""
11장 파일 분할 스크립트
vol-2-part-4-chapter-11.md를 4개 파일로 분할합니다.
"""

import os

# 설정
ORIGINAL_FILE = '/Users/woogis/Workspace/repo/ai-instructions/book/vol-2-part-4-chapter-11.md'
OUTPUT_DIR = '/Users/woogis/Workspace/repo/ai-instructions/book'

def split_chapter_11():
    """11장을 섹션별로 분할합니다."""
    
    print('=== 11장 파일 분할 시작 ===\n')
    
    # 1. 원본 파일 읽기
    print(f'1. 원본 파일 읽기: {ORIGINAL_FILE}')
    try:
        with open(ORIGINAL_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f'   ✅ 파일 크기: {len(content) / 1024:.1f} KB')
        print(f'   ✅ 총 줄 수: {len(content.splitlines())}')
    except Exception as e:
        print(f'   ❌ 오류: {e}')
        return False
    
    # 2. 섹션 경계 찾기
    print('\n2. 섹션 경계 찾기')
    idx_11_1 = content.find('## 11.1')
    idx_11_2 = content.find('## 11.2')
    idx_11_3 = content.find('## 11.3')
    
    print(f'   11.1 시작 위치: {idx_11_1}')
    print(f'   11.2 시작 위치: {idx_11_2}')
    print(f'   11.3 시작 위치: {idx_11_3}')
    
    if idx_11_1 == -1 or idx_11_2 == -1 or idx_11_3 == -1:
        print('   ❌ 섹션을 찾을 수 없습니다!')
        return False
    
    print('   ✅ 모든 섹션 경계 찾기 완료')
    
    # 3. 섹션 추출
    print('\n3. 섹션 추출')
    section_11_1 = content[idx_11_1:idx_11_2].strip()
    section_11_2 = content[idx_11_2:idx_11_3].strip()
    section_11_3 = content[idx_11_3:].strip()
    
    print(f'   11.1 크기: {len(section_11_1) / 1024:.1f} KB ({len(section_11_1.splitlines())} 줄)')
    print(f'   11.2 크기: {len(section_11_2) / 1024:.1f} KB ({len(section_11_2.splitlines())} 줄)')
    print(f'   11.3 크기: {len(section_11_3) / 1024:.1f} KB ({len(section_11_3.splitlines())} 줄)')
    
    # 4. 파일 저장
    print('\n4. 새 파일 생성')
    
    files = [
        ('vol-2-part-4-chapter-11-01.md', section_11_1),
        ('vol-2-part-4-chapter-11-02.md', section_11_2),
        ('vol-2-part-4-chapter-11-03.md', section_11_3),
    ]
    
    for filename, section_content in files:
        filepath = os.path.join(OUTPUT_DIR, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(section_content)
            print(f'   ✅ 생성: {filename}')
        except Exception as e:
            print(f'   ❌ 오류 ({filename}): {e}')
            return False
    
    # 5. 검증
    print('\n5. 파일 검증')
    for filename, _ in files:
        filepath = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f'   ✅ {filename}: {size / 1024:.1f} KB')
        else:
            print(f'   ❌ {filename}: 파일이 없습니다!')
            return False
    
    print('\n=== ✅ 분할 완료! ===')
    print('\n생성된 파일:')
    print('  - vol-2-part-4-chapter-11-01.md (11.1 사고 클러스터 개념)')
    print('  - vol-2-part-4-chapter-11-02.md (11.2 기본 설계 패턴)')
    print('  - vol-2-part-4-chapter-11-03.md (11.3 실전 사례 + 체크리스트)')
    
    return True

if __name__ == '__main__':
    success = split_chapter_11()
    exit(0 if success else 1)