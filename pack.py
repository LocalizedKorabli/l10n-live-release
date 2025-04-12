import os
from typing import List

shall_not_delete: List[str] = []

langs = ['en', 'zh']

forum_exclude_patterns = ['game_logo.svg', 'game_logo_static.svg']
min_include_patterns = ['version.info', 'global.mo']

import fnmatch
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def should_skip(path: Path, patterns: List[str]) -> bool:
    for pat in patterns:
        if fnmatch.fnmatch(path.name, pat) or fnmatch.fnmatch(str(path.relative_to(Path('.'))), pat):
            return True
    return False

def zip_lang(lang_name: str, zip_type: str) -> str:
    lang_path = Path(lang_name)
    version_path = lang_path.joinpath('texts').joinpath('ru').joinpath('LC_MESSAGES').joinpath('version.info')
    with open(version_path, 'r', encoding='utf-8') as f:
        l10_v = f.readline()
    is_min = zip_type == 'min'
    exclude_logo = zip_type == 'forum'
    zip_infix = '' if is_min else '.mod.forum' if exclude_logo else '.mod'
    dst_zip = f'{l10_v}.{lang_name}{zip_infix}.zip'
    print(f'正在生成压缩包：{dst_zip}')
    with ZipFile(dst_zip, 'w', ZIP_DEFLATED) as zf:
        for child in lang_path.rglob('*'):
            if child.is_dir():
                continue
            if not is_min:
                if should_skip(child, forum_exclude_patterns if exclude_logo else []):
                    print(f'已跳过文件：{child}')
                    continue
            else:
                if not should_skip(child, min_include_patterns):
                    print(f'已跳过文件：{child}')
                    continue
            print(f'已包含文件：{child}')
            zf.write(child, child.name if is_min else child.relative_to(lang_path))
    shall_not_delete.append(dst_zip)
    return dst_zip

if __name__ == '__main__':
    for lang in langs:
        # Full
        print(f'已生成压缩包：{zip_lang(lang, "min")}')
        print(f'已生成压缩包：{zip_lang(lang, "forum")}')
        print(f'已生成压缩包：{zip_lang(lang, "full")}')
    for file in os.listdir('.'):
        if not file.endswith('.zip'):
            continue
        if file not in shall_not_delete:
            os.remove(file)
            print(f'已删除压缩包：{file}')
    input('按回车键退出。')
