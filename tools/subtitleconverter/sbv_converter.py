import re

def srt_to_sbv(content):
    sbv_content = ""
    for line in content.splitlines():
        if re.match(r'\d+', line):
            continue
        elif re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
            times = line.replace(',', '.').split(' --> ')
            start_time = times[0]
            end_time = times[1]
            sbv_content += f"{start_time},{end_time}\n"
        else:
            sbv_content += f"{line}\n"
    return sbv_content

def vtt_to_sbv(content):
    sbv_content = ""
    lines = content.splitlines()
    for i in range(len(lines)):
        if '-->' in lines[i]:
            times = lines[i].replace('.', ',').split(' --> ')
            start_time = times[0]
            end_time = times[1]
            sbv_content += f"{start_time},{end_time}\n"
        else:
            sbv_content += f"{lines[i]}\n"
    return sbv_content

def ass_to_sbv(content):
    sbv_content = ""
    for line in content.splitlines():
        if line.startswith("Dialogue:"):
            parts = line.split(',')
            start_time = parts[1].replace('.', ':')
            end_time = parts[2].replace('.', ':')
            text = ','.join(parts[9:]).replace('\\N', '\n').replace('{\\', '').replace('}', '')
            sbv_content += f"{start_time},{end_time}\n{text}\n"
    return sbv_content

def txt_to_sbv(content):
    sbv_content = ""
    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            start_time = f"0:00:0{i//2}"
            end_time = f"0:00:0{i//2 + 1}"
            text = lines[i].replace('\n', '\n')
            sbv_content += f"{start_time},{end_time}\n{text}\n"
    return sbv_content

def ssa_to_sbv(content):
    # Since SSA and ASS have a similar structure, use the same logic as ASS to SBV conversion
    return ass_to_sbv(content)

def sub_to_sbv(content):
    sbv_content = ""
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}:\d{2}', line):
            times = line.split(',')
            start_time = times[0].replace(':', '.', 1)
            end_time = times[1].replace(':', '.', 1)
            sbv_content += f"{start_time},{end_time}\n"
        else:
            sbv_content += f"{line}\n"
    return sbv_content

def dfxp_to_sbv(content):
    sbv_content = ""
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\n')  # Remove HTML tags and replace newline
        sbv_content += f"{start_time},{end_time}\n{text}\n"
    return sbv_content

def stl_to_sbv(content):
    sbv_content = ""
    matches = re.findall(r'TC_IN="([^"]+)" TC_OUT="([^"]+)"[^>]*>(.*?)</Subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\n')  # Remove HTML tags and replace newline
        sbv_content += f"{start_time},{end_time}\n{text}\n"
    return sbv_content

def mpl_to_sbv(content):
    sbv_content = ""
    matches = re.findall(r'\[(\d+)\]\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (num, start, end, text) in enumerate(matches):
        start_time = start.replace(':', '.', 1)
        end_time = end.replace(':', '.', 1)
        sbv_content += f"{start_time},{end_time}\n{text}\n"
    return sbv_content

def usf_to_sbv(content):
    sbv_content = ""
    matches = re.findall(r'<subtitle start="([^"]+)" end="([^"]+)"[^>]*>(.*?)</subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\n')  # Remove HTML tags and replace newline
        sbv_content += f"{start_time},{end_time}\n{text}\n"
    return sbv_content

def lrc_to_sbv(content):
    sbv_content = ""
    matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', content)
    for index, (minutes, seconds, centiseconds, text) in enumerate(matches):
        start_time = f"0:{minutes}:{seconds}.{centiseconds}"
        end_time = f"0:{minutes}:{int(seconds)+1}.{centiseconds}"
        sbv_content += f"{start_time},{end_time}\n{text}\n"
    return sbv_content

def rt_to_sbv(content):
    sbv_content = ""
    matches = re.findall(r'<Time begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</Time>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\n')  # Remove HTML tags and replace newline
        sbv_content += f"{start_time},{end_time}\n{text}\n"
    return sbv_content

def ttml_to_sbv(content):
    sbv_content = ""
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\n')  # Remove HTML tags and replace newline
        sbv_content += f"{start_time},{end_time}\n{text}\n"
    return sbv_content

def cap_to_sbv(content):
    sbv_content = ""
    matches = re.findall(r'(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace(':', '.', 1)
        end_time = end.replace(':', '.', 1)
        sbv_content += f"{start_time},{end_time}\n{text}\n"
    return sbv_content

def convert_to_sbv(content, format):
    if format == "srt":
        return srt_to_sbv(content)
    elif format == "vtt":
        return vtt_to_sbv(content)
    elif format == "ass":
        return ass_to_sbv(content)
    elif format == "txt":
        return txt_to_sbv(content)
    elif format == "ssa":
        return ssa_to_sbv(content)
    elif format == "sub":
        return sub_to_sbv(content)
    elif format == "dfxp":
        return dfxp_to_sbv(content)
    elif format == "stl":
        return stl_to_sbv(content)
    elif format == "mpl":
        return mpl_to_sbv(content)
    elif format == "usf":
        return usf_to_sbv(content)
    elif format == "lrc":
        return lrc_to_sbv(content)
    elif format == "rt":
        return rt_to_sbv(content)
    elif format == "ttml":
        return ttml_to_sbv(content)
    elif format == "cap":
        return cap_to_sbv(content)
    else:
        raise ValueError(f"Unsupported format: {format}")