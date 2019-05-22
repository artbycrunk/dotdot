import os
import shutil
from . import logger

class Path(object):
    def __init__(self, log):
        self.log = logger.Logger()

    def set_base_dir(self, base_dir):
        base_dir = os.path.abspath(os.path.realpath(
            os.path.expanduser(base_dir)))
        if not os.path.exists(base_dir):
            self.log.warn("Nonexistent base dir %s" % (base_dir), step="path: base dir")
        return base_dir

    def exists(self, path):
        """Returns true if the path exists."""
        return os.path.exists(self.expand(path))

    def expand(self, path):
        """Returns and expanded path"""
        return os.path.expandvars(os.path.expanduser(path))

    def is_link(self, path):
        """Returns true if the path is a symbolic link."""
        return os.path.islink(self.expand(path))

    def link_destination(self, path):
        """Returns the destination of the symbolic link."""
        return os.readlink(self.expand(path))

    def relative(self, source, destination):
        """Returns the relative path to get to the source file from the
        destination file."""
        destination_dir = os.path.dirname(destination)
        return os.path.relpath(source, destination_dir)

    def create_parent(self, path):
        success = True
        parent = os.path.abspath(os.path.join(os.path.expanduser(path), os.pardir))
        if not self.exists(parent):
            self.log.debug("Try to create parent: %s " % str(parent), step="path: create")
            try:
                os.makedirs(parent)
                self.log.lowinfo("Created directory %s" % parent, step="path: create")
            except OSError as err:
                self.log.warn("Failed to create directory %s" % parent,
                              step="path: create", err=err)
                success = False
        return success
    
    def remove(self, destination, force=False):
        removed = False
        if self.is_link(destination):
            os.unlink(destination)
            removed = True
        if not removed and force:
            if os.path.isdir(destination):
                shutil.rmtree(destination)
                removed = True
            else:
                os.remove(destination)
                removed = True
        if removed:
            self.log.lowinfo("Removed %s" % destination, step="path: remove")
        return removed
