import re

def srt_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    for line in content.splitlines():
        if re.match(r'\d+', line):
            continue
        elif re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
            times = line.replace(',', '.').split(' --> ')
            start_time = times[0]
            end_time = times[1]
        else:
            text = line.replace('\n', ' ')
            ttml_content += f'  <p begin="{start_time}" end="{end_time}">{text}</p>\n'
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def vtt_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    lines = content.splitlines()
    for i in range(len(lines)):
        if '-->' in lines[i]:
            times = lines[i].replace('.', ',').split(' --> ')
            start_time = times[0]
            end_time = times[1]
            text = lines[i+1].replace('\n', ' ')
            ttml_content += f'  <p begin="{start_time}" end="{end_time}">{text}</p>\n'
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def ass_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    for line in content.splitlines():
        if line.startswith("Dialogue:"):
            parts = line.split(',')
            start_time = parts[1]
            end_time = parts[2]
            text = ','.join(parts[9:]).replace('\\N', ' ').replace('{\\', '').replace('}', '')
            ttml_content += f'  <p begin="{start_time}" end="{end_time}">{text}</p>\n'
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def txt_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            start_time = f"0:00:0{i//2}"
            end_time = f"0:00:0{i//2 + 1}"
            text = lines[i].replace('\n', ' ')
            ttml_content += f'  <p begin="{start_time}" end="{end_time}">{text}</p>\n'
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def ssa_to_ttml(content):
    # Since SSA and ASS have a similar structure, use the same logic as ASS to TTML conversion
    return ass_to_ttml(content)

def sub_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}:\d{2}', line):
            times = line.split(',')
            start_time = times[0]
            end_time = times[1]
            text = times[2].replace('\n', ' ')
            ttml_content += f'  <p begin="{start_time}" end="{end_time}">{text}</p>\n'
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def sbv_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', line):
            start_time, end_time = line.split(',')
            ttml_content += f'  <p begin="{start_time}" end="{end_time}">\n'
        else:
            ttml_content += f"{line}\n"
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def dfxp_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start
        end_time = end
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        ttml_content += f'  <p begin="{start_time}" end="{end_time}">{text}</p>\n'
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def stl_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    matches = re.findall(r'TC_IN="([^"]+)" TC_OUT="([^"]+)"[^>]*>(.*?)</Subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start
        end_time = end
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        ttml_content += f'  <p begin="{start_time}" end="{end_time}">{text}</p>\n'
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def mpl_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    matches = re.findall(r'\[(\d+)\]\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (num, start, end, text) in enumerate(matches):
        start_time = start
        end_time = end
        ttml_content += f'  <p begin="{start_time}" end="{end_time}">{text}</p>\n'
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def usf_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    matches = re.findall(r'<subtitle start="([^"]+)" end="([^"]+)"[^>]*>(.*?)</subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start
        end_time = end
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        ttml_content += f'  <p begin="{start_time}" end="{end_time}">{text}</p>\n'
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def lrc_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', content)
    for index, (minutes, seconds, centiseconds, text) in enumerate(matches):
        start_time = f"0:{minutes}:{seconds}.{centiseconds}"
        ttml_content += f'  <p begin="{start_time}">{text}</p>\n'
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def rt_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    matches = re.findall(r'<Time begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</Time>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start
        end_time = end
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        ttml_content += f'  <p begin="{start_time}" end="{end_time}">{text}</p>\n'
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def cap_to_ttml(content):
    ttml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tt xmlns="http://www.w3.org/ns/ttml">\n<body>\n<div>\n'
    matches = re.findall(r'(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (start, end, text) in enumerate(matches):
        start_time = start
        end_time = end
        ttml_content += f'  <p begin="{start_time}" end="{end_time}">{text}</p>\n'
    ttml_content += '</div>\n</body>\n</tt>'
    return ttml_content

def convert_to_ttml(content, format):
    if format == "srt":
        return srt_to_ttml(content)
    elif format == "vtt":
        return vtt_to_ttml(content)
    elif format == "ass":
        return ass_to_ttml(content)
    elif format == "txt":
        return txt_to_ttml(content)
    elif format == "ssa":
        return ssa_to_ttml(content)
    elif format == "sub":
        return sub_to_ttml(content)
    elif format == "sbv":
        return sbv_to_ttml(content)
    elif format == "dfxp":
        return dfxp_to_ttml(content)
    elif format == "stl":
        return stl_to_ttml(content)
    elif format == "mpl":
        return mpl_to_ttml(content)
    elif format == "usf":
        return usf_to_ttml(content)
    elif format == "lrc":
        return lrc_to_ttml(content)
    elif format == "rt":
        return rt_to_ttml(content)
    elif format == "ttml":
        return ttml_to_ttml(content)
    elif format == "cap":
        return cap_to_ttml(content)
    else:
        raise ValueError(f"Unsupported format: {format}")