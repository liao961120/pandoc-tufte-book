#%%
import os
import shutil
import pathlib
import subprocess
from datetime import datetime
from .utils.pandoc import Pandoc

#------- Setup here ------------#
SOURCE_DIR = pathlib.Path('chapters/')
ASSETS_DIR = pathlib.Path('figures/')
HTML = pathlib.Path('html/')
PUBLISH = pathlib.Path('docs/')


#------- Auto-generated --------#
PUBLISH.mkdir(exist_ok=True)
TEMPLATE_DIR = HTML / 'templates/'
FILTERS = list((HTML / "filters/").glob("*.py"))
STYLES = list((HTML / "css/").glob("*.css"))
SOURCES = list(SOURCE_DIR.glob("*.md"))
ASSETS = list(ASSETS_DIR.rglob("*"))
BIB =  '\n'.join(f"--bibliography={p}" for p in pathlib.Path(".").glob("*.bib"))
DATE = datetime.now().strftime("%d %B, %Y")
PANDOC = Pandoc('pandoc/').path


def make_html():
    make_style()
    make_assets()
    make_chapters()
    make_index()


def make_style():
    with open(PUBLISH / "style.css", 'w', encoding="utf-8") as outfile:
        for fname in STYLES:
            with open(fname) as infile:
                outfile.write(infile.read() + '\n')


def make_assets():
    target = PUBLISH / ASSETS_DIR
    if target.exists(): rm(target)
    target.mkdir()

    for fp in ASSETS:
        if fp.is_dir():
            copytree(fp, target)
        else:
            shutil.copy2(fp, target)


def make_chapter(fp):
    tgt = PUBLISH / (str(fp.stem) + '.html')
    try:
        chapter = int(fp.stem[:2])
    except:
        print(f"[WARNING] invalid file name: {fp}. Should start with dd!")
        chapter = ''
    
    cmd = f"""
        {PANDOC} 
            --to html5 
            --katex 
            --citeproc 
            --template {TEMPLATE_DIR / "tufte.html5"}
            --csl={TEMPLATE_DIR / "chicago-fullnote-bibliography.csl"}
            --metadata link-citations=false 
            {BIB} 
            --strip-comments 
            --katex 
            --from markdown+smart+header_attributes 
            --section-divs 
            --table-of-contents 
            --toc-depth=2 
            --filter ./filters/whitespace.py 
            --filter ./filters/sidenote.py 
            --filter ./filters/numenvs.py 
            --filter pandoc-xnos 
            --css style.css 
            --variable lang="zh-TW" 
            --variable lastupdate="{DATE}" 
            --variable references-section-title="References" 
            --variable chapter-number="{chapter}"
            --shift-heading-level-by=0 
            --number-sections 
            --number-offset={chapter}
            --output={tgt}
            {TEMPLATE_DIR / "shared-macros.tex"} {fp}
    """
    cmd = [x.strip() for x in cmd.strip().split('\n')]
    
    status = os.system(' '.join(cmd))
    if status != 0:
        print(f"[WARNING] Failed to make {fp} to {tgt}")
    return status


def make_chapters():
    for fp in SOURCES: make_chapter(fp)


def make_index():
    tempf = make_index_md()

    cmd = f"""
    {PANDOC}
        --strip-comments
        --toc-depth=2 
        --from markdown+smart 
        --section-divs 
        --to html5 
        --css style.css 
        --variable lang="zh-TW" 
        --variable lastupdate="{DATE}" 
        --template {TEMPLATE_DIR / "index.html5"}
        --output={PUBLISH / "index.html"}
        {tempf}
    """
    cmd = [x.strip() for x in cmd.strip().split('\n')]
    status = os.system(' '.join(cmd))
    if status != 0:
        print(f"[WARNING] Failed to make {fp} to {tgt}")
    
    os.remove(tempf)
    return status


def make_index_md():
    with open(SOURCE_DIR / "index.md", encoding="utf-8") as f:
        md_src = f.read() + '\n\n'

    htmls = sorted(x for x in PUBLISH.glob("*.html") \
        if x.name != "index.html" and 'reference' not in x.stem.lower())

    for fp in htmls:
        title = extract_title(fp)
        try: 
            chap = f'Chapter {int(fp.stem[:2])}: {title}'
        except: 
            chap = title
        md_src += f"1. [{chap}]({fp.name})\n"
    
    tempf = "temp.md"
    with open(tempf, "w", encoding="utf-8") as f:
        f.write(md_src)
    
    return tempf
        


#------------ Utils ------------#
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def rm(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path, ignore_errors=True)


from bs4 import BeautifulSoup


def extract_title(fp):
    with open(fp, encoding="utf-8") as f:
        html = BeautifulSoup(f.read(), 'html.parser')
    return html.title.string