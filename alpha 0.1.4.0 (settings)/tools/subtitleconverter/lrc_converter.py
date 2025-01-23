import re

def srt_to_lrc(content):
    lrc_content = ""
    for line in content.splitlines():
        if re.match(r'\d+', line):
            continue
        elif re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
            times = line.replace(',', '.').split(' --> ')
            start_time = convert_time_to_lrc_format(times[0])
        else:
            text = line.replace('\n', ' ')
            lrc_content += f'[{start_time}]{text}\n'
    return lrc_content

def vtt_to_lrc(content):
    lrc_content = ""
    lines = content.splitlines()
    for i in range(len(lines)):
        if '-->' in lines[i]:
            times = lines[i].replace('.', ',').split(' --> ')
            start_time = convert_time_to_lrc_format(times[0])
            text = lines[i+1].replace('\n', ' ')
            lrc_content += f'[{start_time}]{text}\n'
    return lrc_content

def ass_to_lrc(content):
    lrc_content = ""
    for line in content.splitlines():
        if line.startswith("Dialogue:"):
            parts = line.split(',')
            start_time = convert_time_to_lrc_format(parts[1].replace('.', ':'))
            text = ','.join(parts[9:]).replace('\\N', ' ').replace('{\\', '').replace('}', '')
            lrc_content += f'[{start_time}]{text}\n'
    return lrc_content

def txt_to_lrc(content):
    lrc_content = ""
    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            start_time = convert_time_to_lrc_format(f"0:00:0{i//2}")
            text = lines[i].replace('\n', ' ')
            lrc_content += f'[{start_time}]{text}\n'
    return lrc_content

def ssa_to_lrc(content):
    # Since SSA and ASS have a similar structure, use the same logic as ASS to LRC conversion
    return ass_to_lrc(content)

def sub_to_lrc(content):
    lrc_content = ""
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}:\d{2}', line):
            times = line.split(',')
            start_time = convert_time_to_lrc_format(times[0].replace(':', '.', 1))
            text = times[2].replace('\n', ' ')
            lrc_content += f'[{start_time}]{text}\n'
    return lrc_content

def sbv_to_lrc(content):
    lrc_content = ""
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', line):
            start_time, _ = line.split(',')
            lrc_content += f'[{convert_time_to_lrc_format(start_time)}]\n'
        else:
            lrc_content += f"{line}\n"
    return lrc_content

def dfxp_to_lrc(content):
    lrc_content = ""
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, _, text) in enumerate(matches):
        start_time = convert_time_to_lrc_format(start.replace('.', ':'))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        lrc_content += f'[{start_time}]{text}\n'
    return lrc_content

def stl_to_lrc(content):
    lrc_content = ""
    matches = re.findall(r'TC_IN="([^"]+)" TC_OUT="([^"]+)"[^>]*>(.*?)</Subtitle>', content, re.DOTALL)
    for index, (start, _, text) in enumerate(matches):
        start_time = convert_time_to_lrc_format(start.replace(':', '.', 1))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        lrc_content += f'[{start_time}]{text}\n'
    return lrc_content

def mpl_to_lrc(content):
    lrc_content = ""
    matches = re.findall(r'\[(\d+)\]\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (num, start, _, text) in enumerate(matches):
        start_time = convert_time_to_lrc_format(start.replace(':', '.', 1))
        lrc_content += f'[{start_time}]{text}\n'
    return lrc_content

def usf_to_lrc(content):
    lrc_content = ""
    matches = re.findall(r'<subtitle start="([^"]+)" end="([^"]+)"[^>]*>(.*?)</subtitle>', content, re.DOTALL)
    for index, (start, _, text) in enumerate(matches):
        start_time = convert_time_to_lrc_format(start.replace('.', ':'))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        lrc_content += f'[{start_time}]{text}\n'
    return lrc_content

def rt_to_lrc(content):
    lrc_content = ""
    matches = re.findall(r'<Time begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</Time>', content, re.DOTALL)
    for index, (start, _, text) in enumerate(matches):
        start_time = convert_time_to_lrc_format(start.replace(':', '.', 1))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        lrc_content += f'[{start_time}]{text}\n'
    return lrc_content

def ttml_to_lrc(content):
    lrc_content = ""
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, _, text) in enumerate(matches):
        start_time = convert_time_to_lrc_format(start.replace('.', ':'))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        lrc_content += f'[{start_time}]{text}\n'
    return lrc_content

def cap_to_lrc(content):
    lrc_content = ""
    matches = re.findall(r'(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (start, _, text) in enumerate(matches):
        start_time = convert_time_to_lrc_format(start.replace(':', '.', 1))
        lrc_content += f'[{start_time}]{text}\n'
    return lrc_content

def convert_time_to_lrc_format(time_str):
    """Convert time string (HH:MM:SS.mmm) to LRC format (MM:SS.mm)."""
    parts = time_str.split(':')
    minutes = int(parts[0]) * 60 + int(parts[1])
    seconds, milliseconds = parts[2].split('.')
    return f"{minutes:02}:{seconds}.{milliseconds[:2]}"

def convert_to_lrc(content, format):
    if format == "srt":
        return srt_to_lrc(content)
    elif format == "vtt":
        return vtt_to_lrc(content)
    elif format == "ass":
        return ass_to_lrc(content)
    elif format == "txt":
        return txt_to_lrc(content)
    elif format == "ssa":
        return ssa_to_lrc(content)
    elif format == "sub":
        return sub_to_lrc(content)
    elif format == "sbv":
        return sbv_to_lrc(content)
    elif format == "dfxp":
        return dfxp_to_lrc(content)
    elif format == "stl":
        return stl_to_lrc(content)
    elif format == "mpl":
        return mpl_to_lrc(content)
    elif format == "usf":
        return usf_to_lrc(content)
    elif format == "lrc":
        return lrc_to_lrc(content)
    elif format == "rt":
        return rt_to_lrc(content)
    elif format == "ttml":
        return ttml_to_lrc(content)
    elif format == "cap":
        return cap_to_lrc(content)
    else:
        raise ValueError(f"Unsupported format: {format}")