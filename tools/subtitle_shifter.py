import re

def shift_subtitle(file_path, ms_shift):
    with open(file_path, 'r') as file:
        content = file.readlines()

    shifted_content = []
    for line in content:
        if '-->' in line:
            start, end = line.split(' --> ')
            new_start = shift_time(start, ms_shift)
            new_end = shift_time(end, ms_shift)
            shifted_content.append(f'{new_start} --> {new_end}\n')
        else:
            shifted_content.append(line)

    with open(file_path, 'w') as file:
        file.writelines(shifted_content)

def shift_subtitle_partial(file_path, start_time, end_time, ms_shift):
    with open(file_path, 'r') as file:
        content = file.readlines()

    shifted_content = []
    for line in content:
        if '-->' in line:
            start, end = line.split(' --> ')
            if start >= start_time and end <= end_time:
                new_start = shift_time(start, ms_shift)
                new_end = shift_time(end, ms_shift)
                shifted_content.append(f'{new_start} --> {new_end}\n')
            else:
                shifted_content.append(line)
        else:
            shifted_content.append(line)

    with open(file_path, 'w') as file:
        file.writelines(shifted_content)

def shift_time(time_str, ms_shift):
    time_pattern = re.compile(r'(\d+):(\d+):(\d+),(\d+)')
    match = time_pattern.match(time_str)
    if match:
        hours, minutes, seconds, milliseconds = map(int, match.groups())
        total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds + ms_shift

        new_hours = total_ms // 3600000
        total_ms %= 3600000
        new_minutes = total_ms // 60000
        total_ms %= 60000
        new_seconds = total_ms // 1000
        new_ms = total_ms % 1000

        return f'{new_hours:02}:{new_minutes:02}:{new_seconds:02},{new_ms:03}'
    return time_str
