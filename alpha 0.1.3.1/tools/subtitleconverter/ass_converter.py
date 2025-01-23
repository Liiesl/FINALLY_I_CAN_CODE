import re

def srt_to_ass(content):
    ass_content = "[Script Info]\n"
    ass_content += "Title: Default ASS\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "PlayDepth: 0\n"
    ass_content += "\n[V4+ Styles]\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_content += "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1\n"
    ass_content += "\n[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    for line in content.splitlines():
        if re.match(r'\d+', line):
            continue
        elif re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
            times = line.replace(',', '.').split(' --> ')
            start_time = times[0]
            end_time = times[1]
        else:
            text = line.replace('\n', ' ')
            ass_content += f'Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n'

    return ass_content

def vtt_to_ass(content):
    ass_content = "[Script Info]\n"
    ass_content += "Title: Default ASS\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "PlayDepth: 0\n"
    ass_content += "\n[V4+ Styles]\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_content += "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1\n"
    ass_content += "\n[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    lines = content.splitlines()
    for i in range(len(lines)):
        if '-->' in lines[i]:
            times = lines[i].replace('.', ',').split(' --> ')
            start_time = times[0]
            end_time = times[1]
            text = lines[i+1].replace('\n', ' ')
            ass_content += f'Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n'

    return ass_content

def txt_to_ass(content):
    ass_content = "[Script Info]\n"
    ass_content += "Title: Default ASS\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "PlayDepth: 0\n"
    ass_content += "\n[V4+ Styles]\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_content += "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1\n"
    ass_content += "\n[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            start_time = f"0:00:0{i//2}.00"
            end_time = f"0:00:0{i//2 + 1}.00"
            text = lines[i].replace('\n', ' ')
            ass_content += f'Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n'

    return ass_content

def sbv_to_ass(content):
    ass_content = "[Script Info]\n"
    ass_content += "Title: Default ASS\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "PlayDepth: 0\n"
    ass_content += "\n[V4+ Styles]\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_content += "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1\n"
    ass_content += "\n[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    lines = content.splitlines()
    for i in range(len(lines)):
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', lines[i]):
            start_time, end_time = lines[i].split(',')
            start_time = start_time.replace('.', ':')
            end_time = end_time.replace('.', ':')
            text = lines[i + 1].replace('\n', ' ')
            ass_content += f'Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n'

    return ass_content

def dfxp_to_ass(content):
    ass_content = "[Script Info]\n"
    ass_content += "Title: Default ASS\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "PlayDepth: 0\n"
    ass_content += "\n[V4+ Styles]\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_content += "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1\n"
    ass_content += "\n[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        ass_content += f'Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n'

    return ass_content

def stl_to_ass(content):
    ass_content = "[Script Info]\n"
    ass_content += "Title: Default ASS\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "PlayDepth: 0\n"
    ass_content += "\n[V4+ Styles]\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_content += "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1\n"
    ass_content += "\n[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    matches = re.findall(r'TC_IN="([^"]+)" TC_OUT="([^"]+)"[^>]*>(.*?)</Subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace(':', '.', 1)
        end_time = end.replace(':', '.', 1)
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        ass_content += f'Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n'

    return ass_content

def mpl_to_ass(content):
    ass_content = "[Script Info]\n"
    ass_content += "Title: Default ASS\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "PlayDepth: 0\n"
    ass_content += "\n[V4+ Styles]\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_content += "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1\n"
    ass_content += "\n[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    matches = re.findall(r'\[(\d+)\]\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (num, start, end, text) in enumerate(matches):
        start_time = start.replace(':', '.', 1)
        end_time = end.replace(':', '.', 1)
        ass_content += f'Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n'

    return ass_content

def usf_to_ass(content):
    ass_content = "[Script Info]\n"
    ass_content += "Title: Default ASS\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "PlayDepth: 0\n"
    ass_content += "\n[V4+ Styles]\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_content += "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1\n"
    ass_content += "\n[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    matches = re.findall(r'<subtitle start="([^"]+)" end="([^"]+)"[^>]*>(.*?)</subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        ass_content += f'Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n'

    return ass_content

def lrc_to_ass(content):
    ass_content = "[Script Info]\n"
    ass_content += "Title: Default ASS\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "PlayDepth: 0\n"
    ass_content += "\n[V4+ Styles]\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_content += "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1\n"
    ass_content += "\n[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', content)
    for index, (minutes, seconds, centiseconds, text) in enumerate(matches):
        start_time = f"0:{minutes}:{seconds}.{centiseconds}"
        end_time = f"0:{minutes}:{int(seconds)+1}.{centiseconds}"
        ass_content += f'Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n'

    return ass_content

def rt_to_ass(content):
    ass_content = "[Script Info]\n"
    ass_content += "Title: Default ASS\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "PlayDepth: 0\n"
    ass_content += "\n[V4+ Styles]\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_content += "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1\n"
    ass_content += "\n[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    matches = re.findall(r'<Time begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</Time>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace(':', '.', 1)
        end_time = end.replace(':', '.', 1)
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        ass_content += f'Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n'

    return ass_content

def ttml_to_ass(content):
    ass_content = "[Script Info]\n"
    ass_content += "Title: Default ASS\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "PlayDepth: 0\n"
    ass_content += "\n[V4+ Styles]\n"
    ass_content += (
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, "
        "ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding\n"
    )
    ass_content += (
        "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,"
        "100,100,0,0,1,1,0,2,10,10,10,1\n"
    )
    ass_content += "\n[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        ass_content += f'Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n'

    return ass_content

def cap_to_ass(content):
    ass_content = "[Script Info]\n"
    ass_content += "Title: Default ASS\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "WrapStyle: 0\n"
    ass_content += "PlayDepth: 0\n"
    ass_content += "\n[V4+ Styles]\n"
    ass_content += (
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, "
        "ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding\n"
    )
    ass_content += (
        "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,"
        "100,100,0,0,1,1,0,2,10,10,10,1\n"
    )
    ass_content += "\n[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    matches = re.findall(r'<Caption time="([^"]+)"[^>]*>(.*?)</Caption>', content, re.DOTALL)
    for index, (time, text) in enumerate(matches):
        start_time = time.replace('.', ':')
        end_time = f"0:{int(time.split(':')[1]) + 1}:{time.split(':')[2]}"
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')  # Remove HTML tags and replace newline
        ass_content += f'Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n'

    return ass_content

def convert_to_ass(format, content):
    if format == "srt":
        return srt_to_ass(content)
    elif format == "vtt":
        return vtt_to_ass(content)
    elif format == "txt":
        return txt_to_ass(content)
    elif format == "sbv":
        return sbv_to_ass(content)
    elif format == "dfxp":
        return dfxp_to_ass(content)
    elif format == "stl":
        return stl_to_ass(content)
    elif format == "mpl":
        return mpl_to_ass(content)
    elif format == "usf":
        return usf_to_ass(content)
    elif format == "lrc":
        return lrc_to_ass(content)
    elif format == "rt":
        return rt_to_ass(content)
    elif format == "rt":
        return ttml_to_ass(content)
    elif format == "rt":
        return cap_to_ass(content)
    else:
        raise ValueError("Unsupported format")
