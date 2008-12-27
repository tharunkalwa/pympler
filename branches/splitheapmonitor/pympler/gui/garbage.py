from pympler.gui.graph import GraphBrowser
from pympler.util.stringutils import trunc, pp
import sys
import gc

__all__ = ['GarbageBrowser', 'start_debug_garbage', 'end_debug_garbage']

class GarbageBrowser(GraphBrowser):
    """
    The GarbageBrowser is a GraphBrowser that illustrates the objects building
    reference cycles. The garbage collector is switched to debug mode (all
    identified garbage is stored in 'gc.garbage') and the garbage collector is
    invoked. The collected objects are then illustrated in a directed graph.

    Large graphs can be reduced to the actual cycles by passing 'reduce=True' to
    the constructor. 
    
    It is recommended to disable the garbage collector when using the
    GarbageBrowser.

    >>> import gc
    >>> gc.disable()
    >>> l = []
    >>> l.append(l)
    >>> del l
    >>> gb = GarbageBrowser()
    >>> gb.render('garbage.eps')
    True
    """
    def __init__(self, reduce=False):
        """
        Initialize the GarbageBrowser with the objects identified by the garbage
        collector.
        """
        gc.set_debug(gc.DEBUG_SAVEALL)
        gc.collect()

        GraphBrowser.__init__(self, gc.garbage, reduce)

    def print_stats(self, fobj=sys.stdout):
        """
        Log annotated garbage objects to console or file.
        """
        self.metadata.sort(key=lambda x: x.size)
        self.metadata.reverse()
        fobj.write('%-10s %8s %-12s %-46s\n' % ('id', 'size', 'type', 'representation'))
        for g in self.metadata:
            fobj.write('0x%08x %8d %-12s %-46s\n' % (g.id, g.size, trunc(g.type, 12), 
                trunc(g.str, 46)))
        fobj.write('Garbage: %8d collected objects (%6d in cycles): %12s\n' % \
            (self.count, self.count_in_cycles, pp(self.total_size)))


def start_debug_garbage():
    """
    Turn off garbage collector to analyze *collectable* reference cycles.
    """
    gc.collect()
    gc.disable()


def end_debug_garbage():
    """
    Turn garbage collection on and disable debug output.
    """
    gc.set_debug(0)
    gc.enable()


