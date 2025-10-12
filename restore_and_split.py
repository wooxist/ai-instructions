#!/usr/bin/env python3
"""
11장 복원 및 분할 스크립트
1. 백업 파일을 현재 파일로 복원
2. 섹션별로 분할
"""

import os
import shutil

BOOK_DIR = '/Users/woogis/Workspace/repo/ai-instructions/book'
CURRENT_FILE = os.path.join(BOOK_DIR, 'vol-2-part-4-chapter-11.md')
OLD_FILE = os.path.join(BOOK_DIR, 'vol-2-part-4-chapter-11-old.md')

def restore_and_split():
    """백업 파일을 복원하고 섹션별로 분할합니다."""
    
    print('=== 11장 복원 및 분할 ===\n')
    
    # Step 1: 백업 파일로 복원
    print('Step 1: 백업 파일 복원')
    print(f'  원본: vol-2-part-4-chapter-11-old.md (50.5 KB)')
    print(f'  대상: vol-2-part-4-chapter-11.md')
    
    # 현재 파일을 임시 백업 (손상된 파일 보존)
    damaged_file = CURRENT_FILE + '.damaged'
    shutil.copy2(CURRENT_FILE, damaged_file)
    print(f'  ✅ 손상된 파일 백업: vol-2-part-4-chapter-11.md.damaged')
    
    # 백업 파일을 현재 파일로 복원
    shutil.copy2(OLD_FILE, CURRENT_FILE)
    print(f'  ✅ 백업 파일 복원 완료\n')
    
    # Step 2: 복원된 파일 읽기
    print('Step 2: 복원된 파일 읽기')
    with open(CURRENT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f'  ✅ 파일 크기: {len(content) / 1024:.1f} KB')
    print(f'  ✅ 총 줄 수: {len(content.splitlines())}\n')
    
    # Step 3: 섹션 경계 찾기
    print('Step 3: 섹션 경계 찾기')
    idx_11_1 = content.find('## 11.1')
    idx_11_2 = content.find('## 11.2')
    idx_11_3 = content.find('## 11.3')
    
    print(f'  11.1 시작: {idx_11_1}')
    print(f'  11.2 시작: {idx_11_2}')
    print(f'  11.3 시작: {idx_11_3}')
    
    if idx_11_1 == -1 or idx_11_2 == -1 or idx_11_3 == -1:
        print('  ❌ 섹션을 찾을 수 없습니다!')
        return False
    
    print('  ✅ 모든 섹션 경계 찾기 완료\n')
    
    # Step 4: 섹션 추출
    print('Step 4: 섹션 추출')
    section_11_1 = content[idx_11_1:idx_11_2].strip()
    section_11_2 = content[idx_11_2:idx_11_3].strip()
    section_11_3 = content[idx_11_3:].strip()
    
    print(f'  11.1: {len(section_11_1) / 1024:.1f} KB ({len(section_11_1.splitlines())} 줄)')
    print(f'  11.2: {len(section_11_2) / 1024:.1f} KB ({len(section_11_2.splitlines())} 줄)')
    print(f'  11.3: {len(section_11_3) / 1024:.1f} KB ({len(section_11_3.splitlines())} 줄)\n')
    
    # Step 5: 파일 저장
    print('Step 5: 새 파일 생성')
    
    files = [
        ('vol-2-part-4-chapter-11-01.md', section_11_1),
        ('vol-2-part-4-chapter-11-02.md', section_11_2),
        ('vol-2-part-4-chapter-11-03.md', section_11_3),
    ]
    
    for filename, section_content in files:
        filepath = os.path.join(BOOK_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(section_content)
        print(f'  ✅ {filename}')
    
    print()
    
    # Step 6: 검증
    print('Step 6: 파일 검증')
    for filename, _ in files:
        filepath = os.path.join(BOOK_DIR, filename)
        size = os.path.getsize(filepath)
        print(f'  ✅ {filename}: {size / 1024:.1f} KB')
    
    print('\n' + '='*60)
    print('✅ 복원 및 분할 완료!')
    print('='*60)
    
    print('\n생성된 파일:')
    print('  1. vol-2-part-4-chapter-11-01.md (11.1 사고 클러스터 개념)')
    print('  2. vol-2-part-4-chapter-11-02.md (11.2 기본 설계 패턴)')
    print('  3. vol-2-part-4-chapter-11-03.md (11.3 실전 사례 + 체크리스트)')
    
    print('\n다음 단계:')
    print('  - vol-2-part-4-chapter-11.md 삭제 (원본, 이미 분할됨)')
    print('  - vol-2-part-4-chapter-11-old.md 삭제 (백업)')
    print('  - vol-2-part-4-chapter-11.md.damaged 삭제 (손상된 파일)')
    
    return True

if __name__ == '__main__':
    success = restore_and_split()
    exit(0 if success else 1)