#!/usr/bin/env python3
"""
불필요한 파일 삭제 스크립트
"""

import os

BOOK_DIR = '/Users/woogis/Workspace/repo/ai-instructions/book'
ROOT_DIR = '/Users/woogis/Workspace/repo/ai-instructions'

def cleanup():
    """불필요한 파일들을 삭제합니다."""
    
    print('=== 파일 정리 ===\n')
    
    files_to_delete = [
        (BOOK_DIR, 'vol-2-part-4-chapter-11.md', '원본 파일 (이미 분할됨)'),
        (BOOK_DIR, 'vol-2-part-4-chapter-11-old.md', '백업 파일'),
        (BOOK_DIR, 'vol-2-part-4-chapter-11.md.damaged', '손상된 파일'),
        (ROOT_DIR, 'report_kr.md', '11장에 통합됨'),
    ]
    
    deleted = []
    not_found = []
    
    for directory, filename, description in files_to_delete:
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            os.remove(filepath)
            deleted.append(f'  ✅ {filename} ({size / 1024:.1f} KB) - {description}')
        else:
            not_found.append(f'  ⚠️ {filename} - 파일이 없습니다')
    
    if deleted:
        print('삭제된 파일:')
        for msg in deleted:
            print(msg)
    
    if not_found:
        print('\n찾을 수 없는 파일:')
        for msg in not_found:
            print(msg)
    
    print('\n' + '='*60)
    print('✅ 파일 정리 완료!')
    print('='*60)
    
    print('\n최종 결과:')
    print('  생성된 파일:')
    print('    - vol-2-part-4-chapter-11-00-intro.md (도입부)')
    print('    - vol-2-part-4-chapter-11-01.md (11.1 개념)')
    print('    - vol-2-part-4-chapter-11-02.md (11.2 패턴)')
    print('    - vol-2-part-4-chapter-11-03.md (11.3 사례 + 체크리스트)')
    print(f'\n  삭제된 파일: {len(deleted)}개')

if __name__ == '__main__':
    cleanup()