"""Build everything in the right order. Works in any shell: `python tools/build_all.py`."""
import pathlib, runpy, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
for script in ('build.py', 'kit.py'):
    runpy.run_path(str(HERE / script), run_name='__main__')
