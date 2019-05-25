import os

from ..plugin import BasicPlugin


class Link(BasicPlugin):

    ACTION = "link"

    def process(self, action, links):
        self.process_links(links)

    def process_links(self, links):
        # success = True
        if not links:
            self.log.error("No links provided!")
            return

        for destination, source in links.items():

            destination = self.path.expand(destination)

            relative = self.get_value("relative", source)
            force = self.get_value("force", source)
            relink = self.get_value("relink", source)
            create = self.get_value("create", source)
            # use_glob = self.get_value("glob", source)
            # test = self.get_value("if", source)

            path = self.default_source(destination, source)
            path = self.path.expand(path)

            full_source_path = os.path.join(self.base_dir, path)

            # run a test (if)

            self.log.debug("Processing : %s -> %s" % (full_source_path, destination), step='link: process')

            # verify if source path exists, exit early.
            if not self.path.exists(full_source_path):
                self.log.warn( "Nonexistent target %s -> %s" % (
                    destination, full_source_path), step='link: process')
                continue

            if create:
                self.path.create_parent(destination)

            if force or relink:
                self.delete(path, destination, relative, force)

            self.make_link(path, destination, relative)

    def get_value(self, key, source=None, default=False):
        value = self.defaults.get(key, default)
        if isinstance(source, dict):
            value = source.get(key, value)
        return value

    def default_source(self, destination, source):
        if isinstance(source, dict):
            source = source.get("path", None)

        if not source:
            source = os.path.basename(destination)
            if source.startswith("."):
                source = source[1:]

        return source

    def delete(self, source, destination, relative, force=False):
        success = True
        source = os.path.join(self.base_dir, source)
        destination = self.path.expand(destination)
        if relative:
            source = self.path.relative(source, destination)

        is_link = self.path.is_link(destination)
        
        if ((is_link and self.path.link_destination(destination) != source) or 
            (self.path.exists(destination) and not is_link)):
            try:
                removed = self.path.remove(destination, force)
                if removed:
                    self.log.debug('Removed link %s' % (destination),
                                   step='link: delete')
            except OSError as err:
                self.log.warn("Failed to remove %s" % destination, 
                step='link: delete', err=err)
                success = False
        return success

    def make_link(self, source, destination, relative):
        """Links destination to source."""
        success = False
        source = os.path.join(self.base_dir, source)
        destination = self.path.expand(destination)
        if relative:
            source = self.path.relative(source, destination)
            self.log.debug('Using relative %s' % (source), step='link: make')
        
        if (not self.path.exists(destination) and self.path.is_link(destination) and
                self.path.link_destination(destination) != source):
            self.log.warn('Invalid link %s -> %s' %
                (destination, self.path.link_destination(destination)), step='link: make')
        
        if not self.path.exists(destination) and self.path.exists(source):
            try:
                os.symlink(source, destination)
                self.log.info('Created link %s -> %s' % (destination, source), step='link: make')
                return True
            except OSError as err:
                self.log.error(
                    'Linking failed %s -> %s' % (destination, source), 
                    step='link: make', err=err)
                return success

        if self.path.exists(destination) and not self.path.is_link(destination):
             self.log.warn(
                    '%s already exists but is a regular file or directory' % destination, step='link: make')
                
        if self.path.is_link(destination) and self.path.link_destination(destination) != source:
            self.log.warn('Incorrect link %s -> %s' %
                (destination, self.path.link_destination(destination)), step='link: make')
            
        if not self.path.exists(source):
            self.log.warn('Nonexistent target for %s : %s' %
                    (destination, source), step='link: make')
            return success

        if (self.path.exists(destination) and self.path.is_link(destination) and
                self.path.link_destination(destination) == source):
            self.log.info('Link exists %s -> %s' % (destination, source), step='link: make')
            success = True
        return success
