# text = """
# This stuff is outside
# #start_edit
# This is inside the first
# This is also Inside
# #stop_edit
# This is between two inside sections
# This is also the same as what I just said
# #start_edit
# This is a new inside
# This is another line
# Hello
# Hi
# #stop_edit
# BYE for now
# This is what I am talking about #start_edit this is inline ye haw #stop_edit hey I am at the end
# """
# start_marker = "#start_edit"
# end_marker = "#stop_edit"

# try:
#     validate_markers(text, start_marker, end_marker)
#     sections = parse_sections(text, start_marker, end_marker)
#     print(sections)
# except ValueError as e:
#     print(f"Error: {e}")