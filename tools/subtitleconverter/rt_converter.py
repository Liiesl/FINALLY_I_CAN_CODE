import re

def srt_to_rt(content):
    rt_content = "<rt>\n"
    for line in content.splitlines():
        if re.match(r'\d+', line):
            continue
        elif re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
            times = line.replace(',', '.').split(' --> ')
            start_time = convert_time_to_rt_format(times[0])
            end_time = convert_time_to_rt_format(times[1])
        else:
            text = line.replace('\n', ' ')
            rt_content += f'<Time begin="{start_time}" end="{end_time}">{text}</Time>\n'
    rt_content += "</rt>"
    return rt_content

def vtt_to_rt(content):
    rt_content = "<rt>\n"
    lines = content.splitlines()
    for i in range(len(lines)):
        if '-->' in lines[i]:
            times = lines[i].replace('.', ',').split(' --> ')
            start_time = convert_time_to_rt_format(times[0])
            end_time = convert_time_to_rt_format(times[1])
            text = lines[i+1].replace('\n', ' ')
            rt_content += f'<Time begin="{start_time}" end="{end_time}">{text}</Time>\n'
    rt_content += "</rt>"
    return rt_content

def ass_to_rt(content):
    rt_content = "<rt>\n"
    for line in content.splitlines():
        if line.startswith("Dialogue:"):
            parts = line.split(',')
            start_time = convert_time_to_rt_format(parts[1].replace('.', ':'))
            end_time = convert_time_to_rt_format(parts[2].replace('.', ':'))
            text = ','.join(parts[9:]).replace('\\N', ' ').replace('{\\', '').replace('}', '')
            rt_content += f'<Time begin="{start_time}" end="{end_time}">{text}</Time>\n'
    rt_content += "</rt>"
    return rt_content

def txt_to_rt(content):
    rt_content = "<rt>\n"
    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            start_time = convert_time_to_rt_format(f"0:00:0{i//2}")
            end_time = convert_time_to_rt_format(f"0:00:0{i//2 + 1}")
            text = lines[i].replace('\n', ' ')
            rt_content += f'<Time begin="{start_time}" end="{end_time}">{text}</Time>\n'
    rt_content += "</rt>"
    return rt_content

def ssa_to_rt(content):
    # Since SSA and ASS have a similar structure, use the same logic as ASS to RT conversion
    return ass_to_rt(content)

def sub_to_rt(content):
    rt_content = "<rt>\n"
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}:\d{2}', line):
            times = line.split(',')
            start_time = convert_time_to_rt_format(times[0].replace(':', '.', 1))
            end_time = convert_time_to_rt_format(times[1].replace(':', '.', 1))
            text = times[2].replace('\n', ' ')
            rt_content += f'<Time begin="{start_time}" end="{end_time}">{text}</Time>\n'
    rt_content += "</rt>"
    return rt_content

def sbv_to_rt(content):
    rt_content = "<rt>\n"
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', line):
            start_time, end_time = line.split(',')
            rt_content += f'<Time begin="{convert_time_to_rt_format(start_time)}" end="{convert_time_to_rt_format(end_time)}">\n'
        else:
            rt_content += f"{line}\n"
    rt_content += "</rt>"
    return rt_content

def dfxp_to_rt(content):
    rt_content = "<rt>\n"
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_rt_format(start.replace('.', ':'))
        end_time = convert_time_to_rt_format(end.replace('.', ':'))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        rt_content += f'<Time begin="{start_time}" end="{end_time}">{text}</Time>\n'
    rt_content += "</rt>"
    return rt_content

def stl_to_rt(content):
    rt_content = "<rt>\n"
    matches = re.findall(r'TC_IN="([^"]+)" TC_OUT="([^"]+)"[^>]*>(.*?)</Subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_rt_format(start.replace(':', '.', 1))
        end_time = convert_time_to_rt_format(end.replace(':', '.', 1))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        rt_content += f'<Time begin="{start_time}" end="{end_time}">{text}</Time>\n'
    rt_content += "</rt>"
    return rt_content

def mpl_to_rt(content):
    rt_content = "<rt>\n"
    matches = re.findall(r'\[(\d+)\]\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (num, start, end, text) in enumerate(matches):
        start_time = convert_time_to_rt_format(start.replace(':', '.', 1))
        end_time = convert_time_to_rt_format(end.replace(':', '.', 1))
        rt_content += f'<Time begin="{start_time}" end="{end_time}">{text}</Time>\n'
    rt_content += "</rt>"
    return rt_content

def usf_to_rt(content):
    rt_content = "<rt>\n"
    matches = re.findall(r'<subtitle start="([^"]+)" end="([^"]+)"[^>]*>(.*?)</subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_rt_format(start.replace('.', ':'))
        end_time = convert_time_to_rt_format(end.replace('.', ':'))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        rt_content += f'<Time begin="{start_time}" end="{end_time}">{text}</Time>\n'
    rt_content += "</rt>"
    return rt_content

def lrc_to_rt(content):
    rt_content = "<rt>\n"
    matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', content)
    for index, (minutes, seconds, centiseconds, text) in enumerate(matches):
        start_time = convert_time_to_rt_format(f"0:{minutes}:{seconds}.{centiseconds}")
        rt_content += f'<Time begin="{start_time}">{text}</Time>\n'
    rt_content += "</rt>"
    return rt_content

def ttml_to_rt(content):
    rt_content = "<rt>\n"
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_rt_format(start.replace('.', ':'))
        end_time = convert_time_to_rt_format(end.replace('.', ':'))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        rt_content += f'<Time begin="{start_time}" end="{end_time}">{text}</Time>\n'
    rt_content += "</rt>"
    return rt_content

def cap_to_rt(content):
    rt_content = "<rt>\n"
    matches = re.findall(r'(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_rt_format(start.replace(':', '.', 1))
        end_time = convert_time_to_rt_format(end.replace(':', '.', 1))
        rt_content += f'<Time begin="{start_time}" end="{end_time}">{text}</Time>\n'
    rt_content += "</rt>"
    return rt_content

def convert_time_to_rt_format(time_str):
    """Convert time string (HH:MM:SS.mmm) to RT format (HH:MM:SS.mmm)."""
    parts = time_str.split(':')
    hours = parts[0]
    minutes = parts[1]
    seconds = parts[2].replace('.', ':')
    return f"{hours}:{minutes}:{seconds}"

def convert_to_rt(content, format):
    if format == "srt":
        return srt_to_rt(content)
    elif format == "vtt":
        return vtt_to_rt(content)
    elif format == "ass":
        return ass_to_rt(content)
    elif format == "txt":
        return txt_to_rt(content)
    elif format == "ssa":
        return ssa_to_rt(content)
    elif format == "sub":
        return sub_to_rt(content)
    elif format == "sbv":
        return sbv_to_rt(content)
    elif format == "dfxp":
        return dfxp_to_rt(content)
    elif format == "stl":
        return stl_to_rt(content)
    elif format == "mpl":
        return mpl_to_rt(content)
    elif format == "usf":
        return usf_to_rt(content)
    elif format == "lrc":
        return lrc_to_rt(content)
    elif format == "rt":
        return rt_to_rt(content)
    elif format == "ttml":
        return ttml_to_rt(content)
    elif format == "cap":
        return cap_to_rt(content)
    else:
        raise ValueError(f"Unsupported format: {format}")