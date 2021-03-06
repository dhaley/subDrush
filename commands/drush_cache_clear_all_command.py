import threading
from ..lib.drush import DrushAPI
from ..lib.thread_progress import ThreadProgress

import sublime_plugin


class DrushCacheClearAllCommand(sublime_plugin.WindowCommand):
    """
    A command that clears all caches.
    """
    def run(self):
        drush_api = DrushAPI(self.window.active_view())
        thread = DrushCacheClearAllThread(self.window, drush_api)
        thread.start()
        ThreadProgress(thread,
                       'Clearing all caches',
                       "Cleared all caches for '%s'" %
                       drush_api.get_drupal_root())


class DrushCacheClearAllThread(threading.Thread):
    """
    A thread to clear all caches.
    """
    def __init__(self, window, drush_api):
        self.window = window
        self.drush_api = drush_api
        threading.Thread.__init__(self)

    def run(self):
        args = list()
        args.append('all')
        self.drush_api.run_command('cache-clear', args, list())
