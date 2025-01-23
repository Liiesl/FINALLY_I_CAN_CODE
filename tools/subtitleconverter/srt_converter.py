import re

def vtt_to_srt(content):
    # Remove WEBVTT header and replace VTT timestamps with SRT timestamps
    srt_content = re.sub(r'(\d{2}):(\d{2}):(\d{2})\.(\d{3})', r'\1:\2:\3,\4', content)
    srt_content = srt_content.replace("WEBVTT\n\n", "")
    return srt_content

def ass_to_srt(content):
    # Convert ASS format to SRT format
    srt_content = ""
    events_section = False
    for line in content.splitlines():
        if line.strip().startswith("[Events]"):
            events_section = True
            continue
        if events_section and line.strip().startswith("Dialogue:"):
            parts = line.split(',', 9)
            start_time = parts[1].replace('.', ',')
            end_time = parts[2].replace('.', ',')
            text = parts[9].replace('\N', '\n').replace('{\\', '').replace('}', '')
            srt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    return srt_content

def sub_to_srt(content):
    # Convert SUB format to SRT format
    srt_content = ""
    for index, line in enumerate(content.splitlines()):
        if line.strip().isdigit():
            srt_content += f"{line}\n"
        elif re.match(r'\d{2}:\d{2}:\d{2}:\d{2}', line):
            start_time, end_time = line.split(',')
            srt_content += f"{start_time.replace(':', ',', 1)} --> {end_time.replace(':', ',', 1)}\n"
        else:
            srt_content += f"{line}\n"
    return srt_content

def txt_to_srt(content):
    # Example logic for converting TXT to SRT
    srt_content = ""
    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            srt_content += f"{i//2 + 1}\n"
            srt_content += f"{lines[i]}\n{lines[i+1]}\n\n"
    return srt_content

def ssa_to_srt(content):
    # Convert SSA format to SRT format
    srt_content = ""
    events_section = False
    for line in content.splitlines():
        if line.strip().startswith("[Events]"):
            events_section = True
            continue
        if events_section and line.strip().startswith("Dialogue:"):
            parts = line.split(',', 9)
            start_time = parts[1].replace('.', ',')
            end_time = parts[2].replace('.', ',')
            text = parts[9].replace('\N', '\n').replace('{\\', '').replace('}', '')
            srt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    return srt_content

def sbv_to_srt(content):
    # Convert SBV format to SRT format
    srt_content = ""
    for index, line in enumerate(content.splitlines()):
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3},\d{2}:\d{2}:\d{2}\.\d{3}', line):
            start_time, end_time = line.split(',')
            srt_content += f"{index + 1}\n"
            srt_content += f"{start_time.replace('.', ',')} --> {end_time.replace('.', ',')}\n"
        else:
            srt_content += f"{line}\n"
    return srt_content

def dfxp_to_srt(content):
    # Convert DFXP (TTML) format to SRT format
    srt_content = ""
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ',')
        end_time = end.replace('.', ',')
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        srt_content += f"{index + 1}\n"
        srt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    return srt_content

def stl_to_srt(content):
    # Convert STL format to SRT format
    srt_content = ""
    matches = re.findall(r'TC_IN="([^"]+)" TC_OUT="([^"]+)"[^>]*>(.*?)</Subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ',')
        end_time = end.replace('.', ',')
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        srt_content += f"{index + 1}\n"
        srt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    return srt_content

def mpl_to_srt(content):
    # Convert MPL format to SRT format
    srt_content = ""
    matches = re.findall(r'\[(\d+)\]\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (num, start, end, text) in enumerate(matches):
        start_time = start.replace(':', ',', 1)
        end_time = end.replace(':', ',', 1)
        srt_content += f"{index + 1}\n"
        srt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    return srt_content

def usf_to_srt(content):
    # Convert USF format to SRT format
    srt_content = ""
    matches = re.findall(r'<subtitle start="([^"]+)" end="([^"]+)"[^>]*>(.*?)</subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ',')
        end_time = end.replace('.', ',')
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        srt_content += f"{index + 1}\n"
        srt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    return srt_content

def lrc_to_srt(content):
    # Convert LRC format to SRT format
    srt_content = ""
    matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', content)
    for index, (minutes, seconds, centiseconds, text) in enumerate(matches):
        start_time = f"00:{minutes}:{seconds},{centiseconds}00"
        end_time = f"00:{minutes}:{int(seconds)+1},{centiseconds}00"
        srt_content += f"{index + 1}\n"
        srt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    return srt_content

def rt_to_srt(content):
    # Convert RT format to SRT format
    srt_content = ""
    matches = re.findall(r'<Time begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</Time>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ',')
        end_time = end.replace('.', ',')
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        srt_content += f"{index + 1}\n"
        srt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    return srt_content

def ttml_to_srt(content):
    # Convert TTML format to SRT format
    srt_content = ""
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ',')
        end_time = end.replace('.', ',')
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        srt_content += f"{index + 1}\n"
        srt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    return srt_content

def cap_to_srt(content):
    # Convert CAP format to SRT format
    srt_content = ""
    matches = re.findall(r'(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace(':', ',', 1)
        end_time = end.replace(':', ',', 1)
        srt_content += f"{index + 1}\n"
        srt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    return srt_content

def convert_to_srt(content, format):
    if format == "vtt":
        return vtt_to_srt(content)
    elif format == "ass":
        return ass_to_srt(content)
    elif format == "sub":
        return sub_to_srt(content)
    elif format == "txt":
        return txt_to_srt(content)
    elif format == "ssa":
        return ssa_to_srt(content)
    elif format == "sbv":
        return sbv_to_srt(content)
    elif format == "dfxp":
        return dfxp_to_srt(content)
    elif format == "stl":
        return stl_to_srt(content)
    elif format == "mpl":
        return mpl_to_srt(content)
    elif format == "usf":
        return usf_to_srt(content)
    elif format == "lrc":
        return lrc_to_srt(content)
    elif format == "rt":
        return rt_to_srt(content)
    elif format == "ttml":
        return ttml_to_srt(content)
    elif format == "cap":
        return cap_to_srt(content)
    else:
        raise ValueError(f"Unsupported format: {format}")