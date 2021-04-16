# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import os
import subprocess

mod = "mod4"
terminal = "termite"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),

    Key([mod], 'm', lazy.layout.maximize()),
    Key([mod], 'n', lazy.layout.normalize()),

    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "x", lazy.spawn("rofi -show run"), desc="Launch App with rofi"),
    Key([mod], "c", lazy.spawn("rofi -show window"), desc="Switch window with rofi"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]


# Gruvbox color scheme.      # list number (color[#])
colors = [
    ["#282828", "#282828"],  # 0  # bg
    ["#282828", "#282828"],  # 1  # bg0
    ["#1d2021", "#1d2021"],  # 2  # bg0_h
    ["#32302f", "#32302f"],  # 3  # bg0_s
    ["#3c3836", "#3c3836"],  # 4  # bg1
    ["#504945", "#504945"],  # 5  # bg2
    ["#665c54", "#665c54"],  # 6  # bg3
    ["#7c6f64", "#7c6f64"],  # 7  # bg4
    ["#ebdbb2", "#ebdbb2"],  # 8  # fg
    ["#fbf1c7", "#fbf1c7"],  # 9  # fg0
    ["#ebdbb2", "#ebdbb2"],  # 10 # fg1é
    ["#bdae93", "#bdae93"],  # 12 # fg3
    ["#a89984", "#a89984"],  # 13 # fg4
    ["#cc241d", "#cc241d"],  # 14 # red hard
    ["#fb4934", "#fb4934"],  # 15 # red soft
    ["#98971a", "#98971a"],  # 16 # green hard
    ["#b8bb26", "#b8bb26"],  # 17 # green soft
    ["#d79921", "#d79921"],  # 18 # yellow hard
    ["#fabd2f", "#fabd2f"],  # 19 # yellow soft
    ["#458588", "#458588"],  # 20 # blue hard
    ["#83a598", "#83a598"],  # 21 # blue soft
    ["#b16286", "#b16286"],  # 22 # purple hard
    ["#d3869b", "#d3869b"],  # 23 # purple soft
    ["#689d6a", "#689d6a"],  # 24 # aqua hard
    ["#8ec07c", "#8ec07c"],  # 25 # aqua soft
    ["#d65d0e", "#d65d0e"],  # 26 # orange hard
    ["#FE8019", "#FE8019"],  # 27 # orange soft
    ["#a89984", "#a89984"],  # 28 # gray
    ["#928374", "#928374"],  # 29 # gray bg
]  # window name#

group_names = [
    ("I", {"layout": "Columns"}),
    ("II", {"layout": "Columns"}),
    ("III", {"layout": "Columns"}),
    ("IV", {"layout": "Columns"}),
    ("V", {"layout": "Columns"}),
    ("VI", {"layout": "Columns"}),
]

groups = [Group(name, **kwargs) for name, kwargs in group_names]
key_groups = [i for i in "sdfuiop"]

for i, (name, kwargs) in enumerate(group_names, 0):
    keys.append(
        Key([mod], key_groups[i], lazy.group[name].toscreen())
    )  # Switch to another group
    keys.append(
        Key([mod, "shift"], key_groups[i], lazy.window.togroup(name))
    )  # Send current window to another group

layout_theme = {
    "border_width": 2,
    "margin": 10,
    "border_focus": "#83a598",  # colors list cannot come before this. layouts break.
    "border_normal": "#32302f",
}

layouts = [
    layout.Columns(
        # border_focus_stack='#d75f5f',
        **layout_theme
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(
        # **layout_theme,
        # num_stacks=2),
    # layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.MonadTall(
    #     change_size=20,
    #     change_ratio=0.05,
    #     **layout_theme,
    # ),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
    # layout.Floating(**layout_theme),
]

widget_defaults = dict(
    # font='Meslo bold',
    font='Ubuntu Mono',
    fontsize=12,
    padding=10,
    foreground=colors[8],
    background=colors[2],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper='~/Pictures/Wallpapers/wallpaper.jpeg',
        wallpaper_mode='fill',

        top=bar.Bar(
            [
                widget.TextBox(
                    text='',
                    fontsize=28,
                    padding=4,
                    background=colors[19],
                ),
                widget.CurrentLayout(
                    background=colors[19],
                ),
                widget.TextBox(
                    text = '',
                    background = colors[6],
                    foreground = colors[19],
                    padding = 0,
                    fontsize = 24
                ),
                widget.GroupBox(
                    highlight_method = "line",
                    disable_drag='True',
                    padding=15,
                    background=colors[6],
                ),
                widget.TextBox(
                    text = '',
                    background = colors[0],
                    foreground = colors[6],
                    padding = 0,
                    fontsize = 24
                ),
                widget.Spacer(
                    background=colors[0],
                    opacity=0.1
                ),
                widget.TextBox(
                    text = '',
                    background = colors[0],
                    foreground = colors[23],
                    padding = 0,
                    fontsize = 24
                ),
                widget.TextBox(
                    text='',
                    fontsize=28,
                    background=colors[23],
                ),
                widget.CheckUpdates(
                    # distro = "Arch_checkupdates",
                    update_interval = 1800,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                    background=colors[23],
                ),
                widget.TextBox(
                    text = '',
                    background = colors[23],
                    foreground = colors[15],
                    padding = 0,
                    fontsize = 24
                ),
                widget.Battery(
                    format='{char} {percent:2.0%}',
                    charge_char='',
                    discharge_char='',
                    background=colors[15],
                ),
                widget.TextBox(
                    text = '',
                    background = colors[15],
                    foreground = colors[25],
                    padding = 0,
                    fontsize = 24
                ),
                widget.TextBox(
                    text='',
                    fontsize=28,
                    padding=4,
                    background=colors[25],
                ),
                widget.Volume(
                    channel='Master',
                    background=colors[25],
                ),
                widget.TextBox(
                    text = '',
                    background = colors[25],
                    foreground = colors[19],
                    padding = 0,
                    fontsize = 24
                ),
                widget.TextBox(
                    text='',
                    fontsize=25,
                    padding=4,
                    background=colors[19],
                ),
                widget.Clock(
                    format='%Y-%m-%d %a',
                    background=colors[19],
                ),
                widget.TextBox(
                    text='',
                    fontsize=25,
                    padding=4,
                    background=colors[19],
                ),
                widget.Clock(
                    format='%H:%M',
                    background=colors[19],
                ),
                widget.TextBox(
                    text = '',
                    background = colors[19],
                    foreground = colors[28],
                    padding = 0,
                    fontsize = 24
                ),
                widget.TextBox(
                    text='直',
                    fontsize=28,
                    background=colors[28],
                ),
                widget.Wlan(
                    interface='wlp3s0',
                    format='{quality}%',
                    disconnected_message='',
                    background=colors[28],
                ),
            ],
            24,
            opacity=0.9
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def startup_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

wmname = "Qtile"
