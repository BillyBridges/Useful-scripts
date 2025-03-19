#FOR WINDOWS
import fontforge
import os

#This script opens a FontForge .sfd file and look for class kerning tables.
#Then it looks to add to the classes, the glyphs that reference the glyphs
#already in the class together with them. For example, if a class of a
#kerning subtable contains the character "a", the script will add the cha-
#racters that use the glyph "a" as a reference, like the "atilde", that uses
#the reference to the glyph "a" and glyph "tilde" to compose itself, in or-
#der to kern the glyph "atilde" with the same distances as the glyph "a".
#The objective is to make the kerning process quicker, as you can kern the
#base glyphs with classes, which should be fairly quick, and the script will
#make the corresponding composite glyphs be kerned in the same way as their
#bases.

#The situation with the ligatures has not been solved yet, and are left un-
#processed for manual processing later. Comments and color markings are added
#to the glyphs for easy identification later.

def n_list(data):
    if isinstance(data, tuple):
        data = list(data)  # Convert tuple to list

    if isinstance(data, list):
        for i in range(len(data)):
            data[i] = n_list(data[i])  # Recursive call
    return data

def process_gpos_lookups(font):
    count = 0
    for lookup in font.gpos_lookups:
        count += process_lookup(font, lookup)
    return count

def process_lookup(font, lookup):
    count = 0
    subtables = font.getLookupSubtables(lookup)
    for subtable in subtables:
        count += process_subtable(font, subtable)
    return count

def process_subtable(font, subtable):
    if font.isKerningClass(subtable):
        kern_table = n_list(font.getKerningClass(subtable))
        count = expand_classes(font, kern_table)
        font.alterKerningClass(subtable, kern_table[0], kern_table[1], kern_table[2])
        return count
    return 0

def expand_classes(font, kern_table):
    count = 0
    for ci in [0, 1]:
        if kern_table[ci] is not None:
            count += process_class_list(font, kern_table, ci)
    if (count > 0):
        count += expand_classes(font, kern_table)
    return count

def process_class_list(font, kern_table, ci):
    count = 0
    for _class in kern_table[ci]:
        count += process_class(font, _class, kern_table, ci)
    return count

def process_class(font, _class, kern_table, ci):
    count = 0
    if _class is not None:
        for glyph in font.glyphs():
            count += process_glyph(_class, kern_table, ci, glyph)
    return count

def process_glyph(_class, kern_table, ci, glyph):
    count = 0
    refs_in_class = 0
    if glyph.references:
        for ref in glyph.references:
            if belongs_to_table_class(ref[0], kern_table[0]) or belongs_to_table_class(ref[0], kern_table[1]):
                refs_in_class += 1
        if (refs_in_class == 1):  # Glyph has only one reference in subtables'
                                  # classes, so it's put in that class even if it has
                                  # a reference for another base glyph that is not
                                  # in the subtables' kern classes
            count += process_reference(_class, kern_table, ci, glyph)
        elif (refs_in_class > 1): # Glyph is a ligature so it's not processed.
                                  # Instead it's marked for manual processing later.
            if not("Awaits adhesion to kerning class." in glyph.comment):
                glyph.comment = f"{glyph.comment} | Awaits adhesion to kerning class. Original color: 0x{color_to_hex(glyph.color)} | Times: 1"
            else:
                glyph.comment = increment_counter_in_string(glyph.comment)
            glyph.color = 0xff0000 # Reds glyph to mark as "manual processing pending".
    return count

def process_reference(_class, kern_table, ci, glyph):
    count = 0
    for ref in glyph.references:
        if (ref[0] in _class):
            if not(belongs_to_table_class(glyph.glyphname, kern_table[ci])):
                _class.append(glyph.glyphname)
                if not("Adhered to kerning class:" in glyph.comment):
                    glyph.comment = f"{glyph.comment} | Adhered to kerning class: ({('left' if (ci == 0) else 'right')}){_class} Original color: 0x{color_to_hex(glyph.color)}"
                else:
                    glyph.comment = f"{glyph.comment} | ({('left' if (ci == 0) else 'right')}) {_class}"
                glyph.color = 0x00ff00 # Greens glyph to mark as processed
                count += 1;
    return count

def belongs_to_table_class(glyphname, classset):
    if classset is not None:
        for _cls in classset:
            if _cls is not None:
                if glyphname in _cls:
                    return True
    return False

def increment_counter_in_string(input_string):
    try:
        # 1. Find the start index of the counter:
        start_index = input_string.index("Times: ") + len("Times: ")
        # 2. Extract the counter substring:
        counter_substring = input_string[start_index:]
        # 3. Convert the counter substring to an integer:
        counter = int(counter_substring)
        # 4. Construct and return the new string:
        return input_string[:start_index] + str(counter + 1)
    except ValueError:
        # Handle cases where the counter is not a valid integer:
        return input_string
    except Exception:
        # Handle cases where "Times: " is not found or other unexpected errors:
        return input_string

def color_to_hex(color):
    red = (color >> 16) & 0xFF    # Extract red component
    green = (color >> 8) & 0xFF   # Extract green component
    blue = color & 0xFF         # Extract blue component
    hex_color = f"{red:02x}{green:02x}{blue:02x}"  # Format each component as hex
    return hex_color

if __name__ == "__main__":
    filepath = input("Enter file path: ")
    # Open the font file
    print("Attempting to open file...")
    try:
        font = fontforge.open(filepath, 1+8+16+32)
        print(f'Oppened font "{filepath}"')
        # Process kerning classes
        print("Attempting to expand classes...")
        try:
            print(process_gpos_lookups(font), " glyphs added.")
            # Save the modified font
            print("Attempting to save the modified font...")
            dir_path = os.path.dirname(filepath)
            filename = os.path.basename(filepath)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(dir_path, name + "_modified" + ext)
            try:
                font.save(output_path)
                print(f"Modified font saved to: {output_path}")
            except Exception as e:
                print(f'Unexpected error while saving the font "{output_path}": {e}')
        except Exception as e:
            print(f'Unexpected error while processing the font "{filepath}": {e}')
        # Closes original font
        print("Attempting to close original font...")
        try:
            font.close()
            print(f'Closed font "{filepath}"')
        except Exception as e:
            print(f'Unexpected error while closing the font "{filepath}": {e}')
    except Exception as e:
        print(f'Unexpected error while opening the font "{filepath}": {e}')

