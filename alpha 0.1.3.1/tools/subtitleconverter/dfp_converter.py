import re

def srt_to_dfxp(content):
    dfxp_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dfxp_content += '<tt xmlns="http://www.w3.org/ns/ttml">\n'
    dfxp_content += '  <body>\n'
    dfxp_content += '    <div>\n'

    for line in content.splitlines():
        if re.match(r'\d+', line):
            continue
        elif re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
            times = line.replace(',', '.').split(' --> ')
            start_time = f't{times[0]}s'
            end_time = f't{times[1]}s'
        else:
            text = line.replace('\n', ' ')
            dfxp_content += f'      <p begin="{start_time}" end="{end_time}">{text}</p>\n'

    dfxp_content += '    </div>\n'
    dfxp_content += '  </body>\n'
    dfxp_content += '</tt>'

    return dfxp_content

def vtt_to_dfxp(content):
    dfxp_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dfxp_content += '<tt xmlns="http://www.w3.org/ns/ttml">\n'
    dfxp_content += '  <body>\n'
    dfxp_content += '    <div>\n'

    lines = content.splitlines()
    for i in range(len(lines)):
        if '-->' in lines[i]:
            times = lines[i].replace('.', ',').split(' --> ')
            start_time = f't{times[0]}s'
            end_time = f't{times[1]}s'
            text = lines[i+1].replace('\n', ' ')
            dfxp_content += f'      <p begin="{start_time}" end="{end_time}">{text}</p>\n'

    dfxp_content += '    </div>\n'
    dfxp_content += '  </body>\n'
    dfxp_content += '</tt>'

    return dfxp_content

def txt_to_dfxp(content):
    dfxp_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dfxp_content += '<tt xmlns="http://www.w3.org/ns/ttml">\n'
    dfxp_content += '  <body>\n'
    dfxp_content += '    <div>\n'

    lines = content.splitlines()
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            start_time = f't0:00:0{i//2}.00s'
            end_time = f't0:00:0{i//2 + 1}.00s'
            text = lines[i].replace('\n', ' ')
            dfxp_content += f'      <p begin="{start_time}" end="{end_time}">{text}</p>\n'

    dfxp_content += '    </div>\n'
    dfxp_content += '  </body>\n'
    dfxp_content += '</tt>'

    return dfxp_content

def sbv_to_dfxp(content):
    dfxp_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dfxp_content += '<tt xmlns="http://www.w3.org/ns/ttml">\n'
    dfxp_content += '  <body>\n'
    dfxp_content += '    <div>\n'

    lines = content.splitlines()
    for i in range(len(lines)):
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', lines[i]):
            times = lines[i].split(',')
            start_time = f't{times[0].replace(".", ":")}s'
            end_time = f't{times[1].replace(".", ":")}s'
            text = lines[i + 1].replace('\n', ' ')
            dfxp_content += f'      <p begin="{start_time}" end="{end_time}">{text}</p>\n'

    dfxp_content += '    </div>\n'
    dfxp_content += '  </body>\n'
    dfxp_content += '</tt>'

    return dfxp_content

def sub_to_dfxp(content):
    dfxp_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dfxp_content += '<tt xmlns="http://www.w3.org/ns/ttml">\n'
    dfxp_content += '  <body>\n'
    dfxp_content += '    <div>\n'
    
    for line in content.splitlines():
        if re.match(r'\d{2}:\d{2}:\d{2}:\d{2}', line):
            times = line.split(',')
            start_time = f't{times[0].replace(":", ".")}s'
            end_time = f't{times[1].replace(":", ".")}s'
        else:
            text = line.replace('\n', ' ')
            dfxp_content += f'      <p begin="{start_time}" end="{end_time}">{text}</p>\n'

    dfxp_content += '    </div>\n'
    dfxp_content += '  </body>\n'
    dfxp_content += '</tt>'
    
    return dfxp_content

def ass_to_dfxp(content):
    dfxp_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dfxp_content += '<tt xmlns="http://www.w3.org/ns/ttml">\n'
    dfxp_content += '  <body>\n'
    dfxp_content += '    <div>\n'
    
    for line in content.splitlines():
        if line.startswith("Dialogue:"):
            parts = line.split(',')
            start_time = f't{parts[1].replace(".", ":")}s'
            end_time = f't{parts[2].replace(".", ":")}s'
            text = ','.join(parts[9:]).replace('\\N', ' ').replace('{\\', '').replace('}', '')
            dfxp_content += f'      <p begin="{start_time}" end="{end_time}">{text}</p>\n'

    dfxp_content += '    </div>\n'
    dfxp_content += '  </body>\n'
    dfxp_content += '</tt>'
    
    return dfxp_content

def ssa_to_dfxp(content):
    # SSA and ASS have a similar structure, so we can reuse the ASS conversion logic.
    return ass_to_dfxp(content)

def stl_to_dfxp(content):
    dfxp_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dfxp_content += '<tt xmlns="http://www.w3.org/ns/ttml">\n'
    dfxp_content += '  <body>\n'
    dfxp_content += '    <div>\n'
    
    matches = re.findall(r'TC_IN="([^"]+)" TC_OUT="([^"]+)"[^>]*>(.*?)</Subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = f't{start.replace(".", ":")}s'
        end_time = f't{end.replace(".", ":")}s'
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')
        dfxp_content += f'      <p begin="{start_time}" end="{end_time}">{text}</p>\n'

    dfxp_content += '    </div>\n'
    dfxp_content += '  </body>\n'
    dfxp_content += '</tt>'
    
    return dfxp_content

def idx_to_dfxp(content):
    # IDX typically works with SUB files, so this function will assume the IDX file provided contains similar timing information
    return sub_to_dfxp(content)

def mpl_to_dfxp(content):
    dfxp_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dfxp_content += '<tt xmlns="http://www.w3.org/ns/ttml">\n'
    dfxp_content += '  <body>\n'
    dfxp_content += '    <div>\n'
    
    matches = re.findall(r'\[(\d+)\]\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})\s*(.*)', content)
    for index, (num, start, end, text) in enumerate(matches):
        start_time = f't{start.replace(":", ".")}s'
        end_time = f't{end.replace(":", ".")}s'
        dfxp_content += f'      <p begin="{start_time}" end="{end_time}">{text}</p>\n'

    dfxp_content += '    </div>\n'
    dfxp_content += '  </body>\n'
    dfxp_content += '</tt>'
    
    return dfxp_content

def usf_to_dfxp(content):
    dfxp_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dfxp_content += '<tt xmlns="http://www.w3.org/ns/ttml">\n'
    dfxp_content += '  <body>\n'
    dfxp_content += '    <div>\n'
    
    matches = re.findall(r'<subtitle start="([^"]+)" end="([^"]+)"[^>]*>(.*?)</subtitle>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = f't{start.replace(".", ":")}s'
        end_time = f't{end.replace(".", ":")}s'
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')
        dfxp_content += f'      <p begin="{start_time}" end="{end_time}">{text}</p>\n'

    dfxp_content += '    </div>\n'
    dfxp_content += '  </body>\n'
    dfxp_content += '</tt>'
    
    return dfxp_content

def lrc_to_dfxp(content):
    dfxp_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dfxp_content += '<tt xmlns="http://www.w3.org/ns/ttml">\n'
    dfxp_content += '  <body>\n'
    dfxp_content += '    <div>\n'
    
    matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', content)
    for index, (minutes, seconds, centiseconds, text) in enumerate(matches):
        start_time = f't0:{minutes}:{seconds}.{centiseconds}s'
        end_time = f't0:{minutes}:{int(seconds) + 1}.{centiseconds}s'
        dfxp_content += f'      <p begin="{start_time}" end="{end_time}">{text}</p>\n'

    dfxp_content += '    </div>\n'
    dfxp_content += '  </body>\n'
    dfxp_content += '</tt>'
    
    return dfxp_content

def rt_to_dfxp(content):
    dfxp_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dfxp_content += '<tt xmlns="http://www.w3.org/ns/ttml">\n'
    dfxp_content += '  <body>\n'
    dfxp_content += '    <div>\n'
    
    matches = re.findall(r'<Time begin="([^"]+)" end="([^"]+)"[^>]*>(.*?)</Time>', content, re.DOTALL)
    for index, (start, end, text) in enumerate(matches):
        start_time = f't{start.replace(".", ":")}s'
        end_time = f't{end.replace(".", ":")}s'
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')
        dfxp_content += f'      <p begin="{start_time}" end="{end_time}">{text}</p>\n'

    dfxp_content += '    </div>\n'
    dfxp_content += '  </body>\n'
    dfxp_content += '</tt>'
    
    return dfxp_content

def ttml_to_dfxp(content):
    # TTML is already in the DFXP (TTML) format, so no conversion is needed.
    return content

def cap_to_dfxp(content):
    dfxp_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dfxp_content += '<tt xmlns="http://www.w3.org/ns/ttml">\n'
    dfxp_content += '  <body>\n'
    dfxp_content += '    <div>\n'
    
    matches = re.findall(r'<Caption time="([^"]+)"[^>]*>(.*?)</Caption>', content, re.DOTALL)
    for index, (time, text) in enumerate(matches):
        start_time = f't{time.replace(".", ":")}s'
        end_time = f't0:{int(time.split(":")[1]) + 1}:{time.split(":")[2]}s'
        text = re.sub(r'<[^>]+>', '', text).replace('\n', ' ')
        dfxp_content += f'      <p begin="{start_time}" end="{end_time}">{text}</p>\n'

    dfxp_content += '    </div>\n'
    dfxp_content += '  </body>\n'
    dfxp_content += '</tt>'
    
    return dfxp_content

def convert_to_dfxp(format, content):
    if format == "sub":
        return sub_to_dfxp(content)
    elif format == "srt":
        return srt_to_dfxp(content)
    elif format == "vtt":
        return vtt_to_dfxp(content)
    elif format == "txt":
        return txt_to_dfxp(content)
    elif format == "sbv":
        return sbv_to_dfxp(content)
    elif format == "ass":
        return ass_to_dfxp(content)
    elif format == "ssa":
        return ssa_to_dfxp(content)
    elif format == "stl":
        return stl_to_dfxp(content)
    elif format == "idx":
        return idx_to_dfxp(content)
    elif format == "mpl":
        return mpl_to_dfxp(content)
    elif format == "usf":
        return usf_to_dfxp(content)
    elif format == "lrc":
        return lrc_to_dfxp(content)
    elif format == "rt":
        return rt_to_dfxp(content)
    elif format == "ttml":
        return ttml_to_dfxp(content)
    elif format == "cap":
        return cap_to_dfxp(content)
    else:
        raise ValueError("Unsupported format")
