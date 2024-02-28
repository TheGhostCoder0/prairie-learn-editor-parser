import unittest


def validate_markers(text, start_marker, end_marker):
    editing = False
    start_marker_len = len(start_marker)
    end_marker_len = len(end_marker)

    i = 0
    while i < len(text):
        if text[i:i+start_marker_len] == start_marker:
            if editing:
                raise ValueError("Nested start marker found.")
            editing = True
            i += start_marker_len
        elif text[i:i+end_marker_len] == end_marker:
            if not editing:
                raise ValueError("End marker found without a matching start marker.")
            editing = False
            i += end_marker_len
        else:
            i += 1

    if editing:
        raise ValueError("Start marker found without a matching end marker.")


def parse_sections(text, start_marker, end_marker):
    validate_markers(text, start_marker, end_marker)

    sections = []
    in_section = False
    current_section = []
    start_marker_len = len(start_marker)
    end_marker_len = len(end_marker)

    i = 0
    while i < len(text):
        if text[i:i+start_marker_len] == start_marker:
            current_section.append(text[i:i+start_marker_len])
            in_section = True
            i += start_marker_len
        elif text[i:i+end_marker_len] == end_marker and in_section:
            current_section.append(text[i:i+end_marker_len])
            in_section = False
            section_str = ''.join(current_section)
            section_str = section_str[len(start_marker):-len(end_marker)]
            sections.append(section_str)
            current_section = []
            i += end_marker_len
        else:
            if in_section:
                current_section.append(text[i])
            i += 1

    return sections


class TestParserFunctions(unittest.TestCase):
    def test_basic_single_section(self):
        text = "Apple #start_edit Pear #end_edit Grapes"
        self.assertEqual(parse_sections(text, "#start_edit", "#end_edit"), [" Pear "])

    def test_basic_multi_section(self):
        text = "First #start_edit Section #end_edit Second #start_edit Section #end_edit"
        self.assertEqual(parse_sections(text, "#start_edit", "#end_edit"), [" Section ", " Section "])

    def test_multiline_section(self):
        text = "Start #start_edit\nLine1\nLine2\n#end_edit End"
        self.assertEqual(parse_sections(text, "#start_edit", "#end_edit"), ["\nLine1\nLine2\n"])

    def test_error_nested_sections(self):
        text = "#start_edit #start_edit Nested #end_edit #end_edit"
        self.assertRaises(ValueError, lambda: parse_sections(text, "#start_edit", "#end_edit"))

    # Remaining test cases remain unchanged as they do not involve whitespace handling

    def test_start_at_beginning(self):
        text = "#start_edit Section at beginning #end_edit followed by text"
        self.assertEqual(parse_sections(text, "#start_edit", "#end_edit"), [" Section at beginning "])

    def test_end_at_end(self):
        text = "Text followed by #start_edit section at end #end_edit"
        self.assertEqual(parse_sections(text, "#start_edit", "#end_edit"), [" section at end "])

    def test_inline_edit(self):
        text = "Inline #start_edit edit #end_edit here"
        self.assertEqual(parse_sections(text, "#start_edit", "#end_edit"), [" edit "])

    def test_empty_section(self):
        text = "Before #start_edit#end_edit After"
        self.assertEqual(parse_sections(text, "#start_edit", "#end_edit"), [""])

    def test_unique_markers(self):
        text = "Start **begin_section** Unique markers **end_section** End"
        self.assertEqual(parse_sections(text, "**begin_section**", "**end_section**"), [" Unique markers "])

    def test_partial_marker_in_text(self):
        text = "This has a # but not a start #start_edit marker #end_edit here"
        self.assertEqual(parse_sections(text, "#start_edit", "#end_edit"), [" marker "])

    def test_code_like_comment(self):
        text = "#start_edit\n# Please edit this line\n#end_editprint('Hello World')\n"
        self.assertEqual(parse_sections(text, "#start_edit", "#end_edit"), ["\n# Please edit this line\n"])

    def test_marker_with_special_characters(self):
        text = "Start $$!start!$$ section with special $$!end!$$ markers"
        self.assertEqual(parse_sections(text, "$$!start!$$", "$$!end!$$"), [" section with special "])

    def test_overlapping_markers(self):
        text = "#start#start_edit Overlapping #end#stop_edit markers"
        self.assertEqual(parse_sections(text, "#start_edit", "#stop_edit"), [" Overlapping #end"])

    def test_markers_as_part_of_other_words(self):
        text = "This is a #start_test which is not a marker #start_edit but this is #end_edit"
        self.assertEqual(parse_sections(text, "#start_edit", "#end_edit"), [" but this is "])

    def test_empty_markers(self):
        text = "This should not parse"
        self.assertRaises(ValueError, lambda: parse_sections(text, "", ""))

    def test_error_start_without_end(self):
        text = "Start #start_edit without end"
        self.assertRaises(ValueError, lambda: parse_sections(text, "#start_edit", "#end_edit"))

    def test_error_end_without_start(self):
        text = "End without start #end_edit"
        self.assertRaises(ValueError, lambda: parse_sections(text, "#start_edit", "#end_edit"))

    def test_empty_input(self):
        text = ""
        self.assertEqual(parse_sections(text, "#start_edit", "#end_edit"), [])

    def test_no_sections(self):
        text = "No editable sections here"
        self.assertEqual(parse_sections(text, "#start_edit", "#end_edit"), [])

    def test_fibonacci_editable_section(self):
        fibonacci_source = """
            def Fibonacci(n):
                if n < 0:
                    print("Incorrect input")
                elif n == 0:
                    return 0
                elif n == 1 or n == 2:
                    return 1
                else:
                    return #start_edit # What should this line return??? #end_edit
            """
        expected_output = [" # What should this line return??? "]
        self.assertEqual(parse_sections(fibonacci_source, "#start_edit", "#end_edit"), expected_output)

    def test_fibonacci_parser(self):
        fibonacci_source = """
def Fibonacci(n):
    if n < 0:
        print("Incorrect input")
    #start_edit
    # Correct the elif statement below
    elif n == None:
        return None
    #end_edit
    elif n == 1 or n == 2:
        return 1
    else:
        return #start_edit # What should this line return??? #end_edit
"""
        editable_content = parse_sections(fibonacci_source, "#start_edit", "#end_edit")
        expected_output = [
            "\n    # Correct the elif statement below\n    elif n == None:\n        return None\n    ",
            " # What should this line return??? "
        ]
        self.assertEqual(editable_content, expected_output)


# Running the tests
if __name__ == '__main__':
    unittest.main()

