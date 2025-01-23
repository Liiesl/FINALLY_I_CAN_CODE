import re

def srt_to_sub(content):
    sub_content = ""
    for line in content.splitlines():
        if re.match(r'\d+', line):
            continue
        elif re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
            times = line.replace(',', ':').split(' --> ')
            start_time = times[0]
            end_time = times[1]
            sub_content += f"{start_time},{end_time}\n"
        else:
            sub_content += f"{line}\n"
    return sub_content

def vtt_to_sub(content):
    sub_content = ""
    lines = content.splitlines()
    for i in range(len(lines)):
        if '-->' in lines[i]:
            times = lines[i].replace('.', ':').split(' --> ')
            start_time = times[0]
            end_time = times[1]
            sub_content += f"{start_time},{end_time}\n"
        else:
            sub_content += f"{lines[i]}\n"
    return sub_content

def ass_to_sub(content):
    sub_content = ""
    for line in content.splitlines():
        if line.startswith("Dialogue:"):
            parts = line.split(',')
            start_time = parts[1].replace('.', ':')
            end_time = parts[2].replace('.', ':')
            text = ','.join(parts[9:]).replace('\\N', '\n').replace('{\\', '').replace('}', '')
            sub_content += f"{start_time},{end_time}\n{text}\n"
    return sub_content

def txt_to_sub(content):
    sub_content = ""
    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            start_time = f"0:00:0{i//2}"
            end_time = f"0:00:0{i//2 + 1}"
            text = lines[i].replace('\n', '\n')
            sub_content += f"{start_time},{end_time}\n{text}\n"
    return sub_content

def ssa_to_sub(content):
    # Since SSA and ASS have a similar structure, use the same logic as ASS to SUB conversion
    return ass_to_sub(content)

def sbv_to_sub(content):
    sub_content = ""
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', line):
            start_time, end_time = line.split(',')
            sub_content += f"{start_time.replace('.', ':')},{end_time.replace('.', ':')}\n"
        else:
            sub_content += f"{line}\n"
    return sub_content

def dfxp_to_sub(content):
    sub_content = ""
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\n')  # Remove HTML tags and replace newline
        sub_content += f"{start_time},{end_time}\n{text}\n"
    return sub_content

def stl_to_sub(content):
    sub_content = ""
    matches = re.findall(r'TC_IN="([^"]+)" TC_OUT="([^"]+)"[^>]*>(.*?)</Subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\n')  # Remove HTML tags and replace newline
        sub_content += f"{start_time},{end_time}\n{text}\n"
    return sub_content

def mpl_to_sub(content):
    sub_content = ""
    matches = re.findall(r'\[(\d+)\]\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (num, start, end, text) in enumerate(matches):
        start_time = start.replace(':', '.', 1)
        end_time = end.replace(':', '.', 1)
        sub_content += f"{start_time},{end_time}\n{text}\n"
    return sub_content

def usf_to_sub(content):
    sub_content = ""
    matches = re.findall(r'<subtitle start="([^"]+)" end="([^"]+)"[^>]*>(.*?)</subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\n')  # Remove HTML tags and replace newline
        sub_content += f"{start_time},{end_time}\n{text}\n"
    return sub_content

def lrc_to_sub(content):
    sub_content = ""
    matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', content)
    for index, (minutes, seconds, centiseconds, text) in enumerate(matches):
        start_time = f"0:{minutes}:{seconds}.{centiseconds}"
        end_time = f"0:{minutes}:{int(seconds)+1}.{centiseconds}"
        sub_content += f"{start_time},{end_time}\n{text}\n"
    return sub_content

def rt_to_sub(content):
    sub_content = ""
    matches = re.findall(r'<Time begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</Time>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\n')  # Remove HTML tags and replace newline
        sub_content += f"{start_time},{end_time}\n{text}\n"
    return sub_content

def ttml_to_sub(content):
    sub_content = ""
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\n')  # Remove HTML tags and replace newline
        sub_content += f"{start_time},{end_time}\n{text}\n"
    return sub_content

def cap_to_sub(content):
    sub_content = ""
    matches = re.findall(r'(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace(':', '.', 1)
        end_time = end.replace(':', '.', 1)
        sub_content += f"{start_time},{end_time}\n{text}\n"
    return sub_content

def convert_to_sub(content, format):
    if format == "srt":
        return srt_to_sub(content)
    elif format == "vtt":
        return vtt_to_sub(content)
    elif format == "ass":
        return ass_to_sub(content)
    elif format == "txt":
        return txt_to_sub(content)
    elif format == "ssa":
        return ssa_to_sub(content)
    elif format == "sbv":
        return sbv_to_sub(content)
    elif format == "dfxp":
        return dfxp_to_sub(content)
    elif format == "stl":
        return stl_to_sub(content)
    elif format == "mpl":
        return mpl_to_sub(content)
    elif format == "usf":
        return usf_to_sub(content)
    elif format == "lrc":
        return lrc_to_sub(content)
    elif format == "rt":
        return rt_to_sub(content)
    elif format == "ttml":
        return ttml_to_sub(content)
    elif format == "cap":
        return cap_to_sub(content)
    else:
        raise ValueError(f"Unsupported format: {format}")