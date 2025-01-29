import re
from datetime import datetime, timedelta

def read_file(file_path):
    """Reads the content of a subtitle file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    """Writes content to a subtitle file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def merge_subtitles(main_file_path, secondary_file_paths, color_hex=None):
    """Merges multiple subtitle files into one, ensuring blocks with overlapping timestamps are unified."""
    main_content = read_file(main_file_path)
    secondary_contents = [read_file(path) for path in secondary_file_paths]

    if color_hex:
        if isinstance(color_hex, list):
            if len(color_hex) != len(secondary_contents):
                raise ValueError("Number of colors must match number of secondary files.")
            secondary_contents = [color_subtitles(content, hex) for content, hex in zip(secondary_contents, color_hex)]
        secondary_contents = [color_subtitles(content, color_hex) for content in secondary_contents]

    merged_blocks = parse_subtitle_blocks(main_content)
    for content in secondary_contents:
        secondary_blocks = parse_subtitle_blocks(content)
        for timestamp, text in secondary_blocks.items():
            if timestamp in merged_blocks:
                merged_blocks[timestamp] += '\n' + text
            else:
                merged_blocks[timestamp] = text

    unified_blocks = unify_overlapping_blocks(merged_blocks)
    sorted_unified_blocks = dict(sorted(unified_blocks.items(), key=lambda x: parse_timestamp(x[0].split(' --> ')[0])))
    merged_content = format_subtitle_blocks(sorted_unified_blocks)
    return merged_content

def parse_subtitle_blocks(content):
    """Parses subtitle content into blocks and removes existing numbering."""
    blocks = {}
    pattern = re.compile(r'\d+\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\d+\n|\Z)', re.DOTALL)
    matches = pattern.findall(content)
    for match in matches:
        timestamp, text = match
        text = text.strip()
        if timestamp in blocks:
            blocks[timestamp] += '\n' + text
        else:
            blocks[timestamp] = text
    return blocks

def format_subtitle_blocks(blocks):
    """Formats subtitle blocks into content with corrected numbering."""
    formatted_content = ""
    for index, (timestamp, text) in enumerate(blocks.items(), start=1):
        formatted_content += f"{index}\n{timestamp}\n{text}\n\n"
    return formatted_content.strip()

def color_subtitles(content, color_hex):
    """Colors the subtitle text with the given hex color."""
    def replace_text_with_color(match):
        text = match.group(2).strip()
        return f'{match.group(1)}\n<font color="{color_hex}">{text}</font>'

    colored_content = re.sub(r'(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\d+\n|\Z)', replace_text_with_color, content, flags=re.DOTALL)
    return colored_content

def unify_overlapping_blocks(blocks):
    """Combines subtitle blocks with overlapping timestamps into unified blocks."""
    sorted_blocks = sorted(blocks.items(), key=lambda x: parse_timestamp(x[0].split(' --> ')[0]))
    unified_blocks = {}
    
    current_start = None
    current_end = None
    current_text = ""
    
    for timestamp, text in sorted_blocks:
        start, end = timestamp.split(' --> ')
        start_time = parse_timestamp(start)
        end_time = parse_timestamp(end)
        
        if current_start is None:
            current_start = start_time
            current_end = end_time
            current_text = text
        else:
            if start_time <= current_end:
                current_end = max(current_end, end_time)
                current_text += '\n' + text
            else:
                unified_blocks[f"{format_timestamp(current_start)} --> {format_timestamp(current_end)}"] = current_text
                current_start = start_time
                current_end = end_time
                current_text = text
    
    if current_start is not None:
        unified_blocks[f"{format_timestamp(current_start)} --> {format_timestamp(current_end)}"] = current_text
        
    return unified_blocks

def parse_timestamp(timestamp):
    """Parses a timestamp string into a datetime object."""
    return datetime.strptime(timestamp, "%H:%M:%S,%f")

def format_timestamp(timestamp):
    """Formats a datetime object into a timestamp string."""
    return timestamp.strftime("%H:%M:%S,%f")[:-3]

# Example usage:
if __name__ == "__main__":
    main_file_path = 'main.srt'
    secondary_file_paths = ['secondary1.srt', 'secondary2.srt']
    color_hex = '#FF0000'  # Red color for secondary subtitles

    merged_content = merge_subtitles(main_file_path, secondary_file_paths, color_hex)
    write_file('merged.srt', merged_content)
