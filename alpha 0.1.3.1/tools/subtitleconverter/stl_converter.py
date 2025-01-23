import re

def srt_to_stl(content):
    stl_content = "STL\n"  # STL file header
    count = 0
    for line in content.splitlines():
        if re.match(r'\d+', line):
            count += 1
        elif re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
            times = line.replace(',', '.').split(' --> ')
            start_time = times[0].replace(':', '.')
            end_time = times[1].replace(':', '.')
        else:
            text = line.replace('\n', ' ')
            stl_content += f"{start_time} , {end_time} , {text}\n"
    return stl_content

def vtt_to_stl(content):
    stl_content = "STL\n"  # STL file header
    lines = content.splitlines()
    for i in range(len(lines)):
        if '-->' in lines[i]:
            times = lines[i].replace('.', ',').split(' --> ')
            start_time = times[0].replace(':', '.')
            end_time = times[1].replace(':', '.')
            text = lines[i+1].replace('\n', ' ')
            stl_content += f"{start_time} , {end_time} , {text}\n"
    return stl_content

def ass_to_stl(content):
    stl_content = "STL\n"  # STL file header
    for line in content.splitlines():
        if line.startswith("Dialogue:"):
            parts = line.split(',')
            start_time = parts[1].replace('.', ':')
            end_time = parts[2].replace('.', ':')
            text = ','.join(parts[9:]).replace('\\N', ' ').replace('{\\', '').replace('}', '')
            stl_content += f"{start_time} , {end_time} , {text}\n"
    return stl_content

def txt_to_stl(content):
    stl_content = "STL\n"  # STL file header
    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            start_time = f"0:00:0{i//2}"
            end_time = f"0:00:0{i//2 + 1}"
            text = lines[i].replace('\n', ' ')
            stl_content += f"{start_time} , {end_time} , {text}\n"
    return stl_content

def ssa_to_stl(content):
    # Since SSA and ASS have a similar structure, use the same logic as ASS to STL conversion
    return ass_to_stl(content)

def sub_to_stl(content):
    stl_content = "STL\n"  # STL file header
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}:\d{2}', line):
            times = line.split(',')
            start_time = times[0].replace(':', '.', 1)
            end_time = times[1].replace(':', '.', 1)
            text = times[2].replace('\n', ' ')
            stl_content += f"{start_time} , {end_time} , {text}\n"
    return stl_content

def sbv_to_stl(content):
    stl_content = "STL\n"  # STL file header
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', line):
            start_time, end_time = line.split(',')
            stl_content += f"{start_time.replace('.', ':')} , {end_time.replace('.', ':')} , \n"
        else:
            stl_content += f"{line}\n"
    return stl_content

def dfxp_to_stl(content):
    stl_content = "STL\n"  # STL file header
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        stl_content += f"{start_time} , {end_time} , {text}\n"
    return stl_content

def mpl_to_stl(content):
    stl_content = "STL\n"  # STL file header
    matches = re.findall(r'\[(\d+)\]\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (num, start, end, text) in enumerate(matches):
        start_time = start.replace(':', '.', 1)
        end_time = end.replace(':', '.', 1)
        stl_content += f"{start_time} , {end_time} , {text}\n"
    return stl_content

def usf_to_stl(content):
    stl_content = "STL\n"  # STL file header
    matches = re.findall(r'<subtitle start="([^"]+)" end="([^"]+)"[^>]*>(.*?)</subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        stl_content += f"{start_time} , {end_time} , {text}\n"
    return stl_content

def lrc_to_stl(content):
    stl_content = "STL\n"  # STL file header
    matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', content)
    for index, (minutes, seconds, centiseconds, text) in enumerate(matches):
        start_time = f"0H{minutes}M{seconds}.{centiseconds}S"
        end_time = f"0H{minutes}M{int(seconds)+1}.{centiseconds}S"
        stl_content += f"{start_time} , {end_time} , {text}\n"
    return stl_content

def rt_to_stl(content):
    stl_content = "STL\n"  # STL file header
    matches = re.findall(r'<Time begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</Time>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace(':', '.', 1)
        end_time = end.replace(':', '.', 1)
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        stl_content += f"{start_time} , {end_time} , {text}\n"
    return stl_content

def ttml_to_stl(content):
    stl_content = "STL\n"  # STL file header
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        stl_content += f"{start_time} , {end_time} , {text}\n"
    return stl_content

def cap_to_stl(content):
    stl_content = "STL\n"  # STL file header
    matches = re.findall(r'(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace(':', '.', 1)
        end_time = end.replace(':', '.', 1)
        stl_content += f"{start_time} , {end_time} , {text}\n"
    return stl_content

def convert_to_stl(content, format):
    if format == "srt":
        return srt_to_stl(content)
    elif format == "vtt":
        return vtt_to_stl(content)
    elif format == "ass":
        return ass_to_stl(content)
    elif format == "txt":
        return txt_to_stl(content)
    elif format == "ssa":
        return ssa_to_stl(content)
    elif format == "sub":
        return sub_to_stl(content)
    elif format == "sbv":
        return sbv_to_stl(content)
    elif format == "dfxp":
        return dfxp_to_stl(content)
    elif format == "mpl":
        return mpl_to_stl(content)
    elif format == "usf":
        return usf_to_stl(content)
    elif format == "lrc":
        return lrc_to_stl(content)
    elif format == "rt":
        return rt_to_stl(content)
    elif format == "ttml":
        return ttml_to_stl(content)
    elif format == "cap":
        return cap_to_stl(content)
    else:
        raise ValueError(f"Unsupported format: {format}")