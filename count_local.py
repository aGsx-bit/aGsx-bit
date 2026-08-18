"""
Counts lines of code in local projects (outside GitHub) and stores the
snapshot in cache/local_loc.txt. today.py adds this to the GitHub LOC so
the card's "Lines of Code" shows local + GitHub.

Usage:  edit SCAN_DIRS / EXCLUDE_DIRS below, then run  python count_local.py
Run this whenever the local code changes and commit cache/local_loc.txt.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT = os.path.join(HERE, 'cache', 'local_loc.txt')

SCAN_DIRS = [
    os.path.expanduser(r'~\Desktop'),
    os.path.expanduser('~'),
]

# Sub-trees skipped while walking SCAN_DIRS (case-insensitive).
EXCLUDE_DIRS = {
    # system folders and noise
    'appdata', 'onedrive', 'videos', 'music', 'pictures', 'downloads',
    'documents', 'desktop', '3d objects', 'contacts', 'favorites', 'links',
    'saved games', 'searches', 'sendto', 'start menu', 'templates', 'cookies',
    'nethood', 'printhood', 'recent', 'local settings', 'application data',
    'my documents', '.claude', 'node_modules', '.git', '__pycache__', 'venv',
    '.venv', 'env', 'bin', 'obj', 'debug', 'release', 'dist', 'build',
    'target', '.idea', '.vscode', '.vs', 'packages', 'site-packages',
    '.next', 'out', '.cache', '.nuget', 'vendor', '.tox', '.mypy_cache',
    '.pytest_cache',
    # downloaded third-party tools and wordlists (not my code)
    'seclists', 'seclists-master', 'fuzzdb', 'payloadsallthethings',
    'spiderfoot-4.0', 'golismero', 'sigploit', 'sublist3r-master', 'skiptracer',
    'zap', 'ansel', 'gh-cli', 'herd', 'go', 'burpsuitepro-main',
    'cyberstrikeai-1.6.3', 'cyberstrikeai', 'adminhack-main', 'sqlmap',
    'ysoserial.net', 'discord-quest-completer-win32-x64-2025.10.07',
    'auto clicker', 'creamapi-creaminstaller-lastest-b1', 'creaminstaller',
    'mousewithoutborders', 'maltegobackup', 'fiddler2', 'tor browser',
    'deep live cam', 'bandicam', 'ableton', 'adobe',
    # generic scan output folders (not my code)
    'nuclei_scan_results', 'ftp_dump', 'cpanel_results', 'output',
    'cheat sheet', 'programs',
    # my own repo counted via GitHub instead (avoid double counting)
    'github-profile',
}

EXTENSIONS = {
    '.py', '.c', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.cs', '.java', '.go',
    '.php', '.js', '.mjs', '.ts', '.jsx', '.tsx', '.html', '.htm', '.css',
    '.scss', '.sql', '.sh', '.ps1', '.psm1', '.bat', '.cmd', '.json', '.xml',
    '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.md', '.txt', '.tex',
    '.asm', '.rs', '.lua', '.rb', '.kt', '.swift', '.r', '.proto', '.csv',
    '.log', '.tsv', '.srt',
}

# extensionless files that still count as text
NAME_EXCEPTIONS = {
    'dockerfile', 'makefile', 'jenkinsfile', 'license', 'readme', 'changelog',
}

MAX_FILE_BYTES = 2 * 1024 * 1024  # skip bigger files (dumps, binary blobs)

# Machine-specific excludes (kept out of git): cache/excludes_local.txt,
# one lowercase folder name per line, '#' for comments.
LOCAL_EXCLUDES = os.path.join(HERE, 'cache', 'excludes_local.txt')


def load_local_excludes():
    """Reads extra machine-specific excludes; returns a set of lowercase names."""
    extra = set()
    try:
        with open(LOCAL_EXCLUDES, 'r', encoding='utf-8') as f:
            for ln in f:
                ln = ln.strip().lower()
                if ln and not ln.startswith('#'):
                    extra.add(ln)
    except OSError:
        pass
    return extra


def count_dir(root, exclude):
    """Counts non-blank lines in text files under root. Returns (lines, files)."""
    total, files = 0, 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if os.path.normcase(d) not in exclude]
        for fn in filenames:
            base, ext = os.path.splitext(fn)
            if ext.lower() not in EXTENSIONS and not fn.startswith('.'):
                if base.lower() not in NAME_EXCEPTIONS:
                    continue
            fp = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(fp) > MAX_FILE_BYTES:
                    continue
                with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                    n = sum(1 for ln in f if ln.strip())
            except OSError:
                continue
            total += n
            files += 1
    return total, files


def main():
    exclude = EXCLUDE_DIRS | load_local_excludes()
    totals = {}
    for path in SCAN_DIRS:
        lines, files = count_dir(path, exclude)
        totals[path] = (lines, files)
        print(f'{lines:>12,} lines in {files:>6,} files  <- {path}')

    total = sum(v[0] for v in totals.values())

    prev = 0
    if os.path.exists(SNAPSHOT):
        try:
            with open(SNAPSHOT, 'r', encoding='utf-8') as f:
                prev = next((int(ln.strip()) for ln in f
                             if ln.strip() and not ln.lstrip().startswith('#')), 0)
        except (ValueError, OSError):
            prev = 0

    add = max(0, total - prev)
    dlt = max(0, prev - total)

    with open(SNAPSHOT, 'w', encoding='utf-8') as f:
        f.write('# Local (non-GitHub) lines of code snapshot, written by count_local.py\n'
                '# Format: total non-blank lines, additions since last scan, deletions since last scan\n'
                f'{total}\n{add}\n{dlt}\n')
    print(f'\nTotal local LOC: {total:,}  (+{add:,}, -{dlt:,} since last scan)')
    print(f'Snapshot written to {SNAPSHOT}')


if __name__ == '__main__':
    main()
