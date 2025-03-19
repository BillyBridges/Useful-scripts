_w = 0
count = 0
font = fontforge.activeFont()
for _slot in font.selection:
    glyph = font[_slot]
    _w += glyph.width
    count += 1
fontforge.logWarning(f"Number of glyphs selected: {count}")
fontforge.logWarning(f"Total width of selection: {_w}")
fontforge.logWarning(f"Average width of selection: {_w / count}")