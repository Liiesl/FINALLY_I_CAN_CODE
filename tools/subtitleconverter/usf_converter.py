import re

def srt_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    count = 0
    for line in content.splitlines():
        if re.match(r'\d+', line):
            count += 1
        elif re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
            times = line.replace(',', '.').split(' --> ')
            start_time = convert_time_to_usf_format(times[0])
            end_time = convert_time_to_usf_format(times[1])
        else:
            text = line.replace('\n', ' ')
            usf_content += f'    <subtitle start="{start_time}" stop="{end_time}">{text}</subtitle>\n'
    usf_content += '  </subtitles>\n</usf>'
    return usf_content

def vtt_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    lines = content.splitlines()
    for i in range(len(lines)):
        if '-->' in lines[i]:
            times = lines[i].replace('.', ',').split(' --> ')
            start_time = convert_time_to_usf_format(times[0])
            end_time = convert_time_to_usf_format(times[1])
            text = lines[i+1].replace('\n', ' ')
            usf_content += f'    <subtitle start="{start_time}" stop="{end_time}">{text}</subtitle>\n'
    usf_content += '  </subtitles>\n</usf>'
    return usf_content

def ass_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    for line in content.splitlines():
        if line.startswith("Dialogue:"):
            parts = line.split(',')
            start_time = convert_time_to_usf_format(parts[1].replace('.', ':'))
            end_time = convert_time_to_usf_format(parts[2].replace('.', ':'))
            text = ','.join(parts[9:]).replace('\\N', ' ').replace('{\\', '').replace('}', '')
            usf_content += f'    <subtitle start="{start_time}" stop="{end_time}">{text}</subtitle>\n'
    usf_content += '  </subtitles>\n</usf>'
    return usf_content

def txt_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            start_time = convert_time_to_usf_format(f"0:00:0{i//2}")
            end_time = convert_time_to_usf_format(f"0:00:0{i//2 + 1}")
            text = lines[i].replace('\n', ' ')
            usf_content += f'    <subtitle start="{start_time}" stop="{end_time}">{text}</subtitle>\n'
    usf_content += '  </subtitles>\n</usf>'
    return usf_content

def ssa_to_usf(content):
    # Since SSA and ASS have a similar structure, use the same logic as ASS to USF conversion
    return ass_to_usf(content)

def sub_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}:\d{2}', line):
            times = line.split(',')
            start_time = convert_time_to_usf_format(times[0].replace(':', '.', 1))
            end_time = convert_time_to_usf_format(times[1].replace(':', '.', 1))
            text = times[2].replace('\n', ' ')
            usf_content += f'    <subtitle start="{start_time}" stop="{end_time}">{text}</subtitle>\n'
    usf_content += '  </subtitles>\n</usf>'
    return usf_content

def sbv_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', line):
            start_time, end_time = line.split(',')
            usf_content += f'    <subtitle start="{convert_time_to_usf_format(start_time)}" stop="{convert_time_to_usf_format(end_time)}">\n'
        else:
            usf_content += f"{line}\n"
    usf_content += '  </subtitles>\n</usf>'
    return usf_content

def dfxp_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_usf_format(start.replace('.', ':'))
        end_time = convert_time_to_usf_format(end.replace('.', ':'))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        usf_content += f'    <subtitle start="{start_time}" stop="{end_time}">{text}</subtitle>\n'
    usf_content += '  </subtitles>\n</usf>'
    return usf_content

def stl_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    matches = re.findall(r'TC_IN="([^"]+)" TC_OUT="([^"]+)"[^>]*>(.*?)</Subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_usf_format(start.replace(':', '.', 1))
        end_time = convert_time_to_usf_format(end.replace(':', '.', 1))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        usf_content += f'    <subtitle start="{start_time}" stop="{end_time}">{text}</subtitle>\n'
    return usf_content

def mpl_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    matches = re.findall(r'\[(\d+)\]\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (num, start, end, text) in enumerate(matches):
        start_time = convert_time_to_usf_format(start.replace(':', '.', 1))
        end_time = convert_time_to_usf_format(end.replace(':', '.', 1))
        usf_content += f'    <subtitle start="{start_time}" stop="{end_time}">{text}</subtitle>\n'
    return usf_content

def lrc_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', content)
    for index, (minutes, seconds, centiseconds, text) in enumerate(matches):
        start_time = convert_time_to_usf_format(f"0:{minutes}:{seconds}.{centiseconds}")
        end_time = convert_time_to_usf_format(f"0:{minutes}:{int(seconds)+1}.{centiseconds}")
        usf_content += f'    <subtitle start="{start_time}" stop="{end_time}">{text}</subtitle>\n'
    usf_content += '  </subtitles>\n</usf>'
    return usf_content

def rt_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    matches = re.findall(r'<Time begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</Time>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_usf_format(start.replace(':', '.', 1))
        end_time = convert_time_to_usf_format(end.replace(':', '.', 1))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        usf_content += f'    <subtitle start="{start_time}" stop="{end_time}">{text}</subtitle>\n'
    usf_content += '  </subtitles>\n</usf>'
    return usf_content

def ttml_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_usf_format(start.replace('.', ':'))
        end_time = convert_time_to_usf_format(end.replace('.', ':'))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        usf_content += f'    <subtitle start="{start_time}" stop="{end_time}">{text}</subtitle>\n'
    usf_content += '  </subtitles>\n</usf>'
    return usf_content

def cap_to_usf(content):
    usf_content = '<?xml version="1.0" encoding="UTF-8"?>\n<usf>\n  <subtitles>\n'
    matches = re.findall(r'(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_usf_format(start.replace(':', '.', 1))
        end_time = convert_time_to_usf_format(end.replace(':', '.', 1))
        usf_content += f'    <subtitle start="{start_time}" stop="{end_time}">{text}</subtitle>\n'
    return usf_content

def convert_time_to_usf_format(time_str):
    """Convert time string (HH:MM:SS.mmm) to USF format (HH:MM:SS.mmm)."""
    parts = time_str.split(':')
    hours = parts[0]
    minutes = parts[1]
    seconds = parts[2].replace('.', ':')
    return f"{hours}:{minutes}:{seconds}"

def convert_to_usf(content, format):
    if format == "srt":
        return srt_to_usf(content)
    elif format == "vtt":
        return vtt_to_usf(content)
    elif format == "ass":
        return ass_to_usf(content)
    elif format == "txt":
        return txt_to_usf(content)
    elif format == "ssa":
        return ssa_to_usf(content)
    elif format == "sub":
        return sub_to_usf(content)
    elif format == "sbv":
        return sbv_to_usf(content)
    elif format == "dfxp":
        return dfxp_to_usf(content)
    elif format == "stl":
        return stl_to_usf(content)
    elif format == "mpl":
        return mpl_to_usf(content)
    elif format == "usf":
        return usf_to_usf(content)
    elif format == "lrc":
        return lrc_to_usf(content)
    elif format == "rt":
        return rt_to_usf(content)
    elif format == "ttml":
        return ttml_to_usf(content)
    elif format == "cap":
        return cap_to_usf(content)
    else:
        raise ValueError(f"Unsupported format: {format}")