import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ProExtinction/16256cb7-0ffb-59f1-9ca3-47aeaae4b0ca/scratchpad/tr')
from tw import part
lang, page, start, path = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
last = len(sys.argv) > 5
lines = [l.rstrip('\n') for l in open(path, encoding='utf-8') if l.strip()]
part(lang, page, start, lines, last)
