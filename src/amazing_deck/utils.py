"""Shared helpers — colors, units, text."""
import re
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor


def hex_to_rgb(hex_str):
    """Convert #RRGGBB (or RRGGBB) to RGBColor."""
    s = str(hex_str).lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        return RGBColor(0, 0, 0)
    try:
        return RGBColor(int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
    except ValueError:
        return RGBColor(0, 0, 0)


def emu_to_inches(emu):
    """Convert English Metric Units to inches."""
    if emu is None:
        return None
    return round(emu / 914400, 2)


def slugify(name):
    """Make a filesystem-safe slug from a human name."""
    s = re.sub(r"[^\w\s-]", "", str(name).lower())
    s = re.sub(r"[\s_-]+", "-", s).strip("-")
    return s or "untitled"


def _inches(x):
    return Inches(x)


def _pt(x):
    return Pt(x)
