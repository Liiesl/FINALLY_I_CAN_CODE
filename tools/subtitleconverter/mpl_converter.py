import re

def srt_to_mpl(content):
    mpl_content = ""
    count = 0
    for line in content.splitlines():
        if re.match(r'\d+', line):
            count += 1
        elif re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
            times = line.replace(',', '.').split(' --> ')
            start_time = convert_time_to_frames(times[0])
            end_time = convert_time_to_frames(times[1])
        else:
            text = line.replace('\n', '|')
            mpl_content += f'{{{start_time}}}{{{end_time}}}{text}\n'
    return mpl_content

def vtt_to_mpl(content):
    mpl_content = ""
    lines = content.splitlines()
    for i in range(len(lines)):
        if '-->' in lines[i]:
            times = lines[i].replace('.', ',').split(' --> ')
            start_time = convert_time_to_frames(times[0])
            end_time = convert_time_to_frames(times[1])
            text = lines[i+1].replace('\n', '|')
            mpl_content += f'{{{start_time}}}{{{end_time}}}{text}\n'
    return mpl_content

def ass_to_mpl(content):
    mpl_content = ""
    for line in content.splitlines():
        if line.startswith("Dialogue:"):
            parts = line.split(',')
            start_time = convert_time_to_frames(parts[1].replace('.', ':'))
            end_time = convert_time_to_frames(parts[2].replace('.', ':'))
            text = ','.join(parts[9:]).replace('\\N', '|').replace('{\\', '').replace('}', '')
            mpl_content += f'{{{start_time}}}{{{end_time}}}{text}\n'
    return mpl_content

def txt_to_mpl(content):
    mpl_content = ""
    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            start_time = convert_time_to_frames(f"0:00:0{i//2}")
            end_time = convert_time_to_frames(f"0:00:0{i//2 + 1}")
            text = lines[i].replace('\n', '|')
            mpl_content += f'{{{start_time}}}{{{end_time}}}{text}\n'
    return mpl_content

def ssa_to_mpl(content):
    # Since SSA and ASS have a similar structure, use the same logic as ASS to MPL conversion
    return ass_to_mpl(content)

def sub_to_mpl(content):
    mpl_content = ""
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}:\d{2}', line):
            times = line.split(',')
            start_time = convert_time_to_frames(times[0].replace(':', '.', 1))
            end_time = convert_time_to_frames(times[1].replace(':', '.', 1))
            text = times[2].replace('\n', '|')
            mpl_content += f'{{{start_time}}}{{{end_time}}}{text}\n'
    return mpl_content

def sbv_to_mpl(content):
    mpl_content = ""
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', line):
            start_time, end_time = line.split(',')
            mpl_content += f'{{{convert_time_to_frames(start_time)}}}{{{convert_time_to_frames(end_time)}}}\n'
        else:
            mpl_content += f"{line}\n"
    return mpl_content

def dfxp_to_mpl(content):
    mpl_content = ""
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_frames(start.replace('.', ':'))
        end_time = convert_time_to_frames(end.replace('.', ':'))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '|')  # Remove HTML tags and replace newline
        mpl_content += f'{{{start_time}}}{{{end_time}}}{text}\n'
    return mpl_content

def stl_to_mpl(content):
    mpl_content = ""
    matches = re.findall(r'TC_IN="([^"]+)" TC_OUT="([^"]+)"[^>]*>(.*?)</Subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_frames(start.replace(':', '.', 1))
        end_time = convert_time_to_frames(end.replace(':', '.', 1))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '|')  # Remove HTML tags and replace newline
        mpl_content += f'{{{start_time}}}{{{end_time}}}{text}\n'
    return mpl_content

def usf_to_mpl(content):
    mpl_content = ""
    matches = re.findall(r'<subtitle start="([^"]+)" end="([^"]+)"[^>]*>(.*?)</subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_frames(start.replace('.', ':'))
        end_time = convert_time_to_frames(end.replace('.', ':'))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '|')  # Remove HTML tags and replace newline
        mpl_content += f'{{{start_time}}}{{{end_time}}}{text}\n'
    return mpl_content

def lrc_to_mpl(content):
    mpl_content = ""
    matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', content)
    for index, (minutes, seconds, centiseconds, text) in enumerate(matches):
        start_time = convert_time_to_frames(f"0:{minutes}:{seconds}.{centiseconds}")
        end_time = convert_time_to_frames(f"0:{minutes}:{int(seconds)+1}.{centiseconds}")
        mpl_content += f'{{{start_time}}}{{{end_time}}}{text}\n'
    return mpl_content

def rt_to_mpl(content):
    mpl_content = ""
    matches = re.findall(r'<Time begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</Time>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_frames(start.replace(':', '.', 1))
        end_time = convert_time_to_frames(end.replace(':', '.', 1))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '|')  # Remove HTML tags and replace newline
        mpl_content += f'{{{start_time}}}{{{end_time}}}{text}\n'
    return mpl_content

def ttml_to_mpl(content):
    mpl_content = ""
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_frames(start.replace('.', ':'))
        end_time = convert_time_to_frames(end.replace('.', ':'))
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '|')  # Remove HTML tags and replace newline
        mpl_content += f'{{{start_time}}}{{{end_time}}}{text}\n'
    return mpl_content

def cap_to_mpl(content):
    mpl_content = ""
    matches = re.findall(r'(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (start, end, text) in enumerate(matches):
        start_time = convert_time_to_frames(start.replace(':', '.', 1))
        end_time = convert_time_to_frames(end.replace(':', '.', 1))
        mpl_content += f'{{{start_time}}}{{{end_time}}}{text}\n'
    return mpl_content

def convert_time_to_frames(time_str, fps=25):
    """Convert time string (HH:MM:SS.mmm) to frame number."""
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds, milliseconds = map(int, parts[2].split('.'))
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
    return int(total_seconds * fps)

def convert_to_mpl(content, format):
    if format == "srt":
        return srt_to_mpl(content)
    elif format == "vtt":
        return vtt_to_mpl(content)
    elif format == "ass":
        return ass_to_mpl(content)
    elif format == "txt":
        return txt_to_mpl(content)
    elif format == "ssa":
        return ssa_to_mpl(content)
    elif format == "sub":
        return sub_to_mpl(content)
    elif format == "sbv":
        return sbv_to_mpl(content)
    elif format == "dfxp":
        return dfxp_to_mpl(content)
    elif format == "stl":
        return stl_to_mpl(content)
    elif format == "mpl":
        return mpl_to_mpl(content)
    elif format == "usf":
        return usf_to_mpl(content)
    elif format == "lrc":
        return lrc_to_mpl(content)
    elif format == "rt":
        return rt_to_mpl(content)
    elif format == "ttml":
        return ttml_to_mpl(content)
    elif format == "cap":
        return cap_to_mpl(content)
    else:
        raise ValueError(f"Unsupported format: {format}")