import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

def apply_color_to_line(line, color_hex):
    if color_hex:
        return f'<font color="{color_hex}">{line}</font>'
    return line

def parse_srt(content):
    pattern = re.compile(r'(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s+(.*?)\n(?=\d+\s+\d{2}:\d{2}:\d{2},\d{3}|\Z)', re.DOTALL)
    matches = pattern.findall(content)
    parsed_content = []
    for match in matches:
        if len(match) == 4:
            num, start, end, text = match
            text = text.replace('\r', '').replace('\n', ' ').strip()
            parsed_content.append((num, start, end, text))
    return parsed_content

def format_srt(parsed_content):
    formatted_content = ""
    for index, (num, start, end, text) in enumerate(parsed_content, 1):
        formatted_content += f"{index}\n{start} --> {end}\n{text}\n\n"
    return formatted_content.strip()

def time_to_milliseconds(time_str):
    hours, minutes, seconds = map(float, re.split('[:,]', time_str))
    total_milliseconds = int((hours * 3600 + minutes * 60 + seconds) * 1000)
    return total_milliseconds

def milliseconds_to_time(ms):
    hours, ms = divmod(ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    seconds, milliseconds = divmod(ms, 1000)
    return f"{int(hours):02}:{int(minutes):02}:{seconds:06.3f}".replace('.', ',')

def merge_subtitles_stacked(main_path, secondary_paths, color_hex):
    main_content = read_file(main_path)
    parsed_main = parse_srt(main_content)

    for secondary_path in secondary_paths:
        secondary_content = read_file(secondary_path)
        parsed_secondary = parse_srt(secondary_content)

        for sec_num, sec_start, sec_end, sec_text in parsed_secondary:
            sec_start_ms = time_to_milliseconds(sec_start)
            sec_end_ms = time_to_milliseconds(sec_end)
            overlapping = False

            for main_index, (main_num, main_start, main_end, main_text) in enumerate(parsed_main):
                main_start_ms = time_to_milliseconds(main_start)
                main_end_ms = time_to_milliseconds(main_end)

                # Check for overlap
                if (sec_start_ms <= main_end_ms) and (sec_end_ms >= main_start_ms):
                    overlapping = True
                    colored_sec_text = apply_color_to_line(sec_text, color_hex)
                    # Insert the secondary subtitle right after the main subtitle
                    merged_text = main_text + '\n' + colored_sec_text
                    parsed_main[main_index] = (main_num, main_start, main_end, merged_text)
                    break

            if not overlapping:
                # No overlap, insert the secondary subtitle as is
                colored_sec_text = apply_color_to_line(sec_text, color_hex)
                parsed_main.append((sec_num, sec_start, sec_end, colored_sec_text))

    # Ensure numbering is in order
    numbered_parsed_main = []
    for index, (num, start, end, text) in enumerate(parsed_main, 1):
        numbered_parsed_main.append((str(index), start, end, text))
    
    return format_srt(numbered_parsed_main)