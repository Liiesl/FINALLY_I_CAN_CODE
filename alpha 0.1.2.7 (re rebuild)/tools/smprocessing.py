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
    pattern = re.compile(r'(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s+((?:.*(?:\r\n|\r|\n))*?)\s*(?=\d+\s+\d{2}:\d{2}:\d{2},\d{3}|\Z)', re.DOTALL)
    return [match.groups() for match in pattern.finditer(content)]

def format_srt(parsed_content):
    formatted_content = ""
    for index, (num, start, end, text) in enumerate(parsed_content, 1):
        formatted_content += f"{index}\n{start} --> {end}\n{text.strip()}\n\n"
    return formatted_content.strip()

def time_to_milliseconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    seconds, milliseconds = divmod(seconds * 1000, 1000)
    total_milliseconds = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
    return total_milliseconds

def merge_subtitles_stacked(main_path, secondary_paths, color_hex):
    main_content = read_file(main_path)
    parsed_main = parse_srt(main_content)

    for secondary_path in secondary_paths:
        secondary_content = read_file(secondary_path)
        parsed_secondary = parse_srt(secondary_content)

        for sec_num, sec_start, sec_end, sec_text in parsed_secondary:
            sec_start_ms = time_to_milliseconds(sec_start.split(',')[0])
            closest_index = None
            closest_diff = float('inf')

            for main_index, (main_num, main_start, main_end, main_text) in enumerate(parsed_main):
                main_start_ms = time_to_milliseconds(main_start.split(',')[0])
                diff = abs(main_start_ms - sec_start_ms)
                if diff < closest_diff:
                    closest_index = main_index
                    closest_diff = diff

            if closest_index is not None:
                colored_sec_text = apply_color_to_line(sec_text, color_hex)
                parsed_main[closest_index] = (
                    parsed_main[closest_index][0],  # num
                    parsed_main[closest_index][1],  # start
                    parsed_main[closest_index][2],  # end
                    parsed_main[closest_index][3] + "\n" + colored_sec_text  # text
                )

    return format_srt(parsed_main)