import re

def srt_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType: v4.00\n\n[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\nStyle: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0\n\n[Events]\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    count = 0
    for line in content.splitlines():
        if re.match(r'\d+', line):
            count += 1
        elif re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
            times = line.replace(',', '.').split(' --> ')
            start_time = times[0]
            end_time = times[1]
        else:
            text = line.replace('\n', '\\N')
            ssa_content += f"Dialogue: Marked=0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    return ssa_content

def vtt_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType: v4.00\n\n[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\nStyle: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0\n\n[Events]\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    lines = content.splitlines()
    for i in range(len(lines)):
        if '-->' in lines[i]:
            times = lines[i].replace('.', ',').split(' --> ')
            start_time = times[0]
            end_time = times[1]
            text = lines[i+1].replace('\n', '\\N')
            ssa_content += f"Dialogue: Marked=0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    return ssa_content

def ass_to_ssa(content):
    ssa_content = content.replace("ScriptType: v4.00+", "ScriptType: v4.00")
    ssa_content = ssa_content.replace("[V4+ Styles]", "[V4 Styles]")
    ssa_content = ssa_content.replace("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding", "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding")
    ssa_content = ssa_content.replace("Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1", "Style: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0")
    ssa_content = ssa_content.replace("Dialogue: 0,", "Dialogue: Marked=0,")
    return ssa_content

def sub_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType: v4.00\n\n[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\nStyle: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0\n\n[Events]\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}:\d{2}', line):
            times = line.split(',')
            start_time = times[0].replace(':', '.', 1)
            end_time = times[1].replace(':', '.', 1)
            text = times[2].replace('\n', '\\N')
            ssa_content += f"Dialogue: Marked=0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    return ssa_content

def txt_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType: v4.00\n\n[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\nStyle: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0\n\n[Events]\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            start_time = f"0:00:0{i//2}"
            end_time = f"0:00:0{i//2 + 1}"
            text = lines[i].replace('\n', '\\N')
            ssa_content += f"Dialogue: Marked=0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    return ssa_content

def sbv_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType: v4.00\n\n[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\nStyle: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0\n\n[Events]\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', line):
            start_time, end_time = line.split(',')
            ssa_content += f"Dialogue: Marked=0,{start_time.replace('.', ':')},{end_time.replace('.', ':')},Default,,0,0,0,,\n"
        else:
            ssa_content += f"{line}\n"
    return ssa_content

def dfxp_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType: v4.00\n\n[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\nStyle: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0\n\n[Events]\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\\N')  # Remove HTML tags and replace newline
        ssa_content += f"Dialogue: Marked=0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    return ssa_content

def stl_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType: v4.00\n\n[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\nStyle: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0\n\n[Events]\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    matches = re.findall(r'TC_IN="([^"]+)" TC_OUT="([^"]+)"[^>]*>(.*?)</Subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\\N')  # Remove HTML tags and replace newline
        ssa_content += f"Dialogue: Marked=0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    return ssa_content

def mpl_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType: v4.00\n\n[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\nStyle: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0\n\n[Events]\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    matches = re.findall(r'\[(\d+)\]\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (num, start, end, text) in enumerate(matches):
        start_time = start.replace(':', '.', 1)
        end_time = end.replace(':', '.', 1)
        ssa_content += f"Dialogue: Marked=0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    return ssa_content

def usf_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType: v4.00\n\n[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\nStyle: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0\n\n[Events]\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    matches = re.findall(r'<subtitle start="([^"]+)" end="([^"]+)"[^>]*>(.*?)</subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\\N')  # Remove HTML tags and replace newline
        ssa_content += f"Dialogue: Marked=0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    return ssa_content

def lrc_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType: v4.00\n\n[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\nStyle: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0\n\n[Events]\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', content)
    for index, (minutes, seconds, centiseconds, text) in enumerate(matches):
        start_time = f"0:{minutes}:{seconds}.{centiseconds}"
        end_time = f"0:{minutes}:{int(seconds)+1}.{centiseconds}"
        ssa_content += f"Dialogue: Marked=0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    return ssa_content

def rt_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType: v4.00\n\n[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\nStyle: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0\n\n[Events]\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    matches = re.findall(r'<Time begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</Time>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\\N')  # Remove HTML tags and replace newline
        ssa_content += f"Dialogue: Marked=0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    return ssa_content

def ttml_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType: v4.00\n\n[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\nStyle: Default,Arial,20,16777215,0,16777215,0,-1,0,1,1,0,2,10,10,10,0,0\n\n[Events]\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    matches = re.findall(r'<p begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</p>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = start.replace('.', ':')
        end_time = end.replace('.', ':')
        text = re.sub(r'<[^>]+>', '', text).replace('\n', '\\N')  # Remove HTML tags and replace newline
        ssa_content += f"Dialogue: Marked=0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    return ssa_content

def cap_to_ssa(content):
    ssa_content = "[Script Info]\nTitle: Default SSA\nScriptType