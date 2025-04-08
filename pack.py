from typing import List

langs = ['en', 'zh']

forum_patterns = ['game_logo.svg', 'game_logo_static.svg']

import fnmatch
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def should_skip(path: Path, patterns: List[str]) -> bool:
    """判断某个路径是否需要排除"""
    for pat in patterns:
        if fnmatch.fnmatch(path.name, pat) or fnmatch.fnmatch(str(path.relative_to(Path('.'))), pat):
            return True
    return False

def zip_lang(lang: str, exclude_logo: bool) -> str:
    """递归打包目录，排除指定模式"""
    lang_path = Path(lang)
    version_path = lang_path.joinpath('texts').joinpath('ru').joinpath('LC_MESSAGES').joinpath('version.info')
    with open(version_path, 'r', encoding='utf-8') as f:
        l10_v = f.readline()
    zip_infix = '.forum' if exclude_logo else ''
    dst_zip = f'{l10_v}.{lang}.mod{zip_infix}.zip'
    with ZipFile(dst_zip, "w", ZIP_DEFLATED) as zf:
        for file in lang_path.rglob("*"):
            if file.is_dir():
                continue
            if should_skip(file, forum_patterns if exclude_logo else []):
                print(f"已跳过：{file}")  # 调试用
                continue
            zf.write(file, file.relative_to(lang_path))
    return dst_zip

if __name__ == "__main__":
    for lang in langs:
        # Full
        print(f"已生成压缩包: {zip_lang(lang, False)}")
        print(f"已生成压缩包: {zip_lang(lang, True)}")
    input('按回车键退出。')
