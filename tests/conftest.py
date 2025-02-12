import sys
from pathlib import Path

# Add the src directory to the system path
src_path = str(Path(__file__).parent.parent)
sys.path.append(src_path)
