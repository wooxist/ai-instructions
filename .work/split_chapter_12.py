#!/usr/bin/env python3
"""
12장 파일을 6개 섹션으로 분할하는 스크립트
"""

def split_chapter_12():
    # 파일 경로
    source_file = '/Users/woogis/Workspace/repo/ai-instructions/book/vol-2-part-4-chapter-12.md'
    
    # 파일 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 섹션 경계 찾기
    sections = {
        '00-intro': ('# 12장:', '## 12.1'),
        '01': ('## 12.1', '## 12.2'),
        '02': ('## 12.2', '## 12.3'),
        '03': ('## 12.3', '## 12.4'),
        '04': ('## 12.4', '## 12.5'),
        '05': ('## 12.5', '---END---')  # 12.5는 파일 끝까지
    }
    
    print("=== 섹션 경계 찾기 ===\n")
    
    for section_id, (start_marker, end_marker) in sections.items():
        start_idx = content.find(start_marker)
        
        if end_marker == '---END---':
            end_idx = len(content)
        else:
            end_idx = content.find(end_marker)
        
        if start_idx == -1:
            print(f"❌ {section_id}: 시작 마커 '{start_marker}' 를 찾을 수 없습니다")
            continue
        
        if end_idx == -1 and end_marker != '---END---':
            print(f"❌ {section_id}: 종료 마커 '{end_marker}' 를 찾을 수 없습니다")
            continue
        
        section_content = content[start_idx:end_idx]
        section_size = len(section_content)
        
        # 파일 저장
        output_file = f'/Users/woogis/Workspace/repo/ai-instructions/book/vol-2-part-4-chapter-12-{section_id}.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(section_content)
        
        print(f"✓ {section_id}: {section_size:,} characters → {output_file}")
    
    print("\n=== 분할 완료 ===")

if __name__ == '__main__':
    split_chapter_12()
