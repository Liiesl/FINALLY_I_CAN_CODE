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

def convert_to_dfxp(format, content):
    if format == "srt":
        return srt_to_dfxp(content)
    elif format == "vtt":
        return vtt_to_dfxp(content)
    elif format == "txt":
        return txt_to_dfxp(content)
    elif format == "sbv":
        return sbv_to_dfxp(content)
    else:
        raise ValueError("Unsupported format")
