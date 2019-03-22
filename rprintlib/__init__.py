from .rpmain import Rtdout, Rprint
import sys
rprint = Rprint() # predefined self-storage Rprint
sprint = Rprint() # predefined stdout Rprint
sprint.rtdout.stdout = sys.stdout

__all__ = ['Rprint', 'Rtdout', 'rprint', 'sprint']
__version__ = "0.7"