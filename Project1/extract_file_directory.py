import os

def print_directory_structure(root_dir, indent=""):
    """지정된 디렉토리의 구조를 출력합니다."""
    # 현재 디렉토리와 하위 파일/폴더 추출
    entries = sorted(os.listdir(root_dir))  # 알파벳 순 정렬
    for i, entry in enumerate(entries):
        # 마지막 항목 여부 확인
        is_last = (i == len(entries) - 1)
        # 출력 포맷 설정
        prefix = "└── " if is_last else "├── "
        # 현재 경로 생성
        entry_path = os.path.join(root_dir, entry)
        print(f"{indent}{prefix}{entry}")
        # 하위 디렉토리 재귀 호출
        if os.path.isdir(entry_path):
            new_indent = indent + ("    " if is_last else "│   ")
            print_directory_structure(entry_path, new_indent)

# 프로젝트 루트 디렉토리 설정
project_root = os.path.abspath("Project1")  # 필요한 경우 경로 수정
print(f"{os.path.basename(project_root)}/")
print_directory_structure(project_root)
