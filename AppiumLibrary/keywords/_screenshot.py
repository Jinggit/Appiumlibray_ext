# -*- coding: utf-8 -*-

import os
import Image
import robot
from keywordgroup import KeywordGroup

class _ScreenshotKeywords(KeywordGroup):

    def __init__(self):
        self._screenshot_index = 0

    # Public

    def capture_page_screenshot(self, filename=None):
        """Takes a screenshot of the current page and embeds it into the log.

        `filename` argument specifies the name of the file to write the
        screenshot into. If no `filename` is given, the screenshot is saved into file
        `appium-screenshot-<counter>.png` under the directory where
        the Robot Framework log file is written into. The `filename` is
        also considered relative to the same directory, if it is not
        given in absolute format.

        `css` can be used to modify how the screenshot is taken. By default
        the bakground color is changed to avoid possible problems with
        background leaking when the page layout is somehow broken.
        """
        path, link = self._get_screenshot_paths(filename)

        if hasattr(self._current_application(), 'get_screenshot_as_file'):
          self._current_application().get_screenshot_as_file(path)
        else:
          self._current_application().save_screenshot(path)

        # Image is shown on its own row and thus prev row is closed on purpose
        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (link, link))

    #public by Guanhua.jing@ekuaibao.com
    def capture_partial_screenshot(self, locator, filename=None):
        """Takes a partial screenshot of the current page and embeds it into the log.
        locator support xpath. Added by Guanhua.jing@nexio.com
        """
        path, link = self._get_screenshot_paths(filename)
        self._capturepartialscreenshot(self._current_application(), locator, path)
        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (link, link))

    #private by Guanhua.jing@ekuaibao.com
    def _capturepartialscreenshot(self, driver, locator, output):
        element = driver.find_element_by_xpath(locator)
        location = element.location
        size = element.size
        driver.save_screenshot(output)
        im = Image.open(output)
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        im = im.crop((int(left), int(top), int(right), int(bottom)))
        im.save(output)
        del im

    # Private

    def _get_screenshot_paths(self, filename):
        if not filename:
            self._screenshot_index += 1
            filename = 'appium-screenshot-%d.png' % self._screenshot_index
        else:
            filename = filename.replace('/', os.sep)
        logdir = self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link
