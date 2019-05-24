import sys


class Color(object):
    NONE = ""
    RESET = "\033[0m"
    RED = "\033[91m" 
    RED_BG = "\033[41m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[0;90m"


class Level(object):
    NOTSET = 0
    DEBUG = 10
    LOWINFO = 15
    INFO = 20
    WARNING = 30
    ERROR = 40

    @classmethod
    def get_color(self, level, colorized=True, bg=False):
        if not colorized:
            return ""
        elif level < Level.DEBUG:
            return ""
        elif Level.DEBUG <= level < Level.LOWINFO:
            return Color.CYAN
        elif Level.LOWINFO <= level < Level.INFO:
            return Color.DARK_GRAY
        elif Level.INFO <= level < Level.WARNING:
            return Color.GREEN
        elif Level.WARNING <= level < Level.ERROR:
            return Color.YELLOW
        elif Level.ERROR <= level:
            return Color.RED if not bg else Color.RED_BG

    @classmethod
    def get_reset(self, colorized=True):
        if not colorized:
            return ""
        return Color.RESET

    @classmethod
    def get_level(self, level):
        level_dict = {
            "debug": self.DEBUG,
            "lowinfo": self.LOWINFO,
            "info": self.INFO,
            "warn": self.WARNING,
            "error": self.ERROR,
        }
        return level_dict.get(level)


class Logger(object):
    __instance = None
    def __new__(cls):
        if Logger.__instance is None:
            Logger.__instance = object.__new__(cls)
            Logger.__instance.level = Level.LOWINFO
            Logger.__instance.colorized = True
        return Logger.__instance

    def set_colorized(self, mode):
        self.colorized = mode
    
    def set_level(self, level):
        if not level:
            level = Level.LOWINFO
        self.level = level

    def log(self, level, message, step=None, err=None):

        level_num = Level.get_level(level)
        if level == "lowinfo":  level = "info"
        if level == "debug": level = ''
        
        if level_num >= self.level:
            use_color = self.colorized and sys.stdout.isatty()
            _step = (("[%s] " % step) if step else "").ljust(16)
            _level = (("%s " % level.upper()) if level else "").rjust(8)
            message = "%s%s" % (_step, message)
            print(
                "%s%s%s %s%s%s"
                % (
                    Level.get_color(level_num, use_color, bg=True),
                    _level,
                    Level.get_reset(use_color),
                    Level.get_color(level_num, use_color),
                    message,
                    Level.get_reset(use_color),
                )
            )
            if err:
                self.debug(err, step=step)

    def debug(self, message, step=None, err=None):
        self.log("debug", message, step=step, err=err)

    def lowinfo(self, message, step=None, err=None):
        self.log("lowinfo", message, step=step, err=err)

    def info(self, message, step=None, err=None):
        self.log("info", message, step=step, err=err)

    def warn(self, message, step=None, err=None):
        self.log("warn", message, step=step, err=err)

    def error(self, message, step=None, err=None):
        self.log("error", message, step=step, err=err)

