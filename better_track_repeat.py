# -*- coding: utf-8 -*-
"""PlayOrder plugin that infinitely repeats a song.

However, this is unlike the default "repeat song" play order
which stops all playback if the user's "song list" changes.

In this plugin, if the user's song list changes and the currently
playing song ends, the first song in the new song list will 
automatically play (repeatedly).

(In contrast, the default "repeat song" play order will stop 
all playback once the current song ends if the song list changes.)
"""

from gi.repository import Gtk

from quodlibet.plugins.playorder import PlayOrderPlugin, PlayOrderInOrderMixin
from quodlibet.plugins import PluginConfigMixin


class BetterTrackRepeatOrder(PlayOrderPlugin,
                             PlayOrderInOrderMixin, PluginConfigMixin):
    PLUGIN_ID = "better_track_repeat"
    PLUGIN_NAME = _("Better Track Repeat")
    PLUGIN_ICON = "gtk-refresh"
    PLUGIN_DESC = _("Repeat song unless song list changes. "
                    "Continue playback in new song list, unlike default repeat behavior.")

    @classmethod
    def PluginPreferences(cls, parent):
        """Setup the plugin's preferences dialog in the Plugins selector.

        :param parent:
        :return: A Gtk VBox holding all the information about this plugin.
        """
        vb = Gtk.VBox(spacing=10)
        vb.set_border_width(10)
        hbox = Gtk.HBox(spacing=6)
        lbl = Gtk.Label(label=_("Number of times to play each song: 無限"))
        hbox.pack_start(lbl, False, True, 0)
        vb.pack_start(hbox, True, True, 0)
        vb.show_all()
        return vb

    def next(self, playlist, iter):
        """OrderInOrder's next() implementation is close but not sufficient for
        repeat playback with a fallback if the song cannot be repeated (for example,
        if the song list changes).

        We return the iter to repeat the current song. However, if the user's
        song list changed, then iter might be None.

        :param playlist: The current playlist.
        :param iter: Iter representing the song that just played in the playlist.
        Can be None if the just-played song doesn't exist in the playlist.
        :return: An iterable representing the next song to play.
        """
        if iter is not None:
            return iter
        else:
            return super(BetterTrackRepeatOrder, self).next(playlist, iter)

    def next_implicit(self, playlist, iter):
        """Called when a song ends passively, e.g. it plays through.

        For this plugin, it is sufficient to simply invoke self.next().

        :param playlist: The current playlist.
        :param iter: Iter representing the song that just played in the playlist.
        Can be None if the just-played song doesn't exist in the playlist.
        :return: An iterable representing the next song to play.
        """
        return self.next(playlist, iter)

    def next_explicit(self, playlist, iter):
        """Called when a song ends explicitly, e.g. the user pressed "Next Song".

        For this plugin, it is sufficient to simply invoke self.next().

        :param playlist: The current playlist.
        :param iter: Iter representing the song that just played in the playlist.
        Can be None if the just-played song doesn't exist in the playlist.
        :return: An iterable representing the next song to play.
        """
        return self.next(playlist, iter)
