#!/usr/bin/env python3
"""
백업 파일 확인 및 복원 스크립트
"""

import os
import shutil

BOOK_DIR = '/Users/woogis/Workspace/repo/ai-instructions/book'
CURRENT_FILE = os.path.join(BOOK_DIR, 'vol-2-part-4-chapter-11.md')
OLD_FILE = os.path.join(BOOK_DIR, 'vol-2-part-4-chapter-11-old.md')

def check_and_restore():
    """백업 파일을 확인하고 필요시 복원합니다."""
    
    print('=== 파일 상태 확인 ===\n')
    
    # 현재 파일 확인
    if os.path.exists(CURRENT_FILE):
        size = os.path.getsize(CURRENT_FILE)
        print(f'현재 파일: vol-2-part-4-chapter-11.md')
        print(f'  크기: {size / 1024:.1f} KB')
        
        with open(CURRENT_FILE, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            print(f'  첫 줄: {first_line[:80]}...')
    
    print()
    
    # 백업 파일 확인
    if os.path.exists(OLD_FILE):
        size = os.path.getsize(OLD_FILE)
        print(f'백업 파일: vol-2-part-4-chapter-11-old.md')
        print(f'  크기: {size / 1024:.1f} KB')
        
        with open(OLD_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()
            print(f'  총 줄 수: {len(lines)}')
            print(f'  첫 줄: {lines[0][:80]}...' if lines else '  (빈 파일)')
        
        # 섹션 확인
        print(f'\n  섹션 확인:')
        print(f'    ## 11.1 위치: {content.find("## 11.1")}')
        print(f'    ## 11.2 위치: {content.find("## 11.2")}')
        print(f'    ## 11.3 위치: {content.find("## 11.3")}')
        
        # 백업 파일이 완전하면 복원 제안
        if content.find("## 11.1") != -1 and content.find("## 11.2") != -1:
            print(f'\n  ✅ 백업 파일이 완전합니다!')
            print(f'\n복원하시겠습니까? (yes/no): ', end='')
            response = input().strip().lower()
            
            if response == 'yes':
                # 현재 파일을 임시 백업
                temp_file = CURRENT_FILE + '.temp'
                shutil.copy2(CURRENT_FILE, temp_file)
                print(f'\n  현재 파일을 {temp_file}에 임시 백업')
                
                # 백업 파일을 현재 파일로 복원
                shutil.copy2(OLD_FILE, CURRENT_FILE)
                print(f'  ✅ 백업 파일을 현재 파일로 복원 완료!')
                
                # 검증
                with open(CURRENT_FILE, 'r', encoding='utf-8') as f:
                    restored_content = f.read()
                    print(f'\n  복원된 파일 크기: {len(restored_content) / 1024:.1f} KB')
                    print(f'  ## 11.1 위치: {restored_content.find("## 11.1")}')
                    print(f'  ## 11.2 위치: {restored_content.find("## 11.2")}')
                    print(f'  ## 11.3 위치: {restored_content.find("## 11.3")}')
                
                return True
            else:
                print('\n  복원을 취소했습니다.')
                return False
        else:
            print(f'\n  ⚠️ 백업 파일도 불완전합니다.')
            return False
    else:
        print(f'백업 파일이 없습니다: vol-2-part-4-chapter-11-old.md')
        return False

if __name__ == '__main__':
    check_and_restore()