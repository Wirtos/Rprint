from .rpmain import Rtdout, Rprint, ARprint, CRprint
import sys
rprint = Rprint() # predefined self-storage Rprint
sprint = Rprint() # predefined stdout Rprint
aprint = ARprint() # predefined async Rprint
cprint = CRprint() # predefined classic-output Rprint
sprint.rtdout.stdout = sys.stdout

__all__ = ['Rprint', 'ARprint', 'CRprint', 'Rtdout', 'rprint', 'sprint', 'aprint', 'cprint']
__version__ = "1.3"