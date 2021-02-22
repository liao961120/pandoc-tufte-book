# Pandoc Tufte Book Template

This repo is created from [`mrtzh/unbuch`](https://github.com/mrtzh/unbuch), wrapped into Python 3 for cross-platform usage.


## Usage

1. [Dowload](https://github.com/liao961120/pandoc-tufte-book/archive/main.zip) the repo
2. Install dependencies:
   
   ```sh
   pip install -r requirements.txt
   ```

3. Build HTML book:

   ```sh
   python3 make.py
   ```


## Modifications

- The original templates from `mrtzh/unbuch` are moved into `html/`
- A Pandoc executable is automatically downloaded when excecuting `make.py` for the first time (i.e., doesn't use the installed Pandoc on your computer)
- Cross-referencing is based on [`tomduck/pandoc-xnos`](https://github.com/tomduck/pandoc-xnos)
   - [Syntax summary](https://github.com/liao961120/ntuthesis2#%E8%AB%96%E6%96%87%E6%92%B0%E5%AF%AB%E6%96%87%E5%85%A7%E8%B6%85%E9%80%A3%E7%B5%90) (in Chinese)
   - Refer to `tomduck/pandoc-xnos` for details.