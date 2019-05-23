from . import logger
import copy
import os
from .path import Path

class BasicPlugin(object):
    def __init__(self, base_dir, defaults=None):
        self.log = logger.Logger()
        self.base_dir = self.path.set_base_dir(base_dir)

        self._defaults = dict()
        if defaults:
            self.set_defaults(defaults)

        if not hasattr(self, "ACTION"):
            self.ACTION = "basic"

    @property
    def path(self):
        if not hasattr(self, "_path"):
            self._path = Path(self.log)
        return self._path

    def set_defaults(self, defaults):
        self._defaults = defaults.get(self.ACTION, {})

    @property
    def defaults(self):
        return copy.deepcopy(self._defaults)

    def process(self, action, data):
        raise NotImplementedError