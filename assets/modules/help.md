# Introduction

Welcome to the application! This is a brief introduction to help you get started.

## Getting Started

Follow these steps to get started with the application:

1. Open the application.
2. Navigate to the settings.
3. Customize your preferences.

## Advanced Features

This section covers advanced features of the application.

### Feature 1

Description of feature 1.

### Feature 2

Description of feature 2.

## Troubleshooting

If you encounter any issues, try the following:

- Restart the application.
- Check your internet connection.
- Contact support.

# WhisperAI Extension for Subtl and Python GUI Applications

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A standalone WhisperAI extension for Python GUI applications, featuring pre-bundled models for speech-to-text subtitling. Primarily developed for [Subtl](https://github.com/your-subtl-repo) but compatible with any Python 3 GUI framework.

![Python GUI Integration](assets/python-demo.gif) <!-- Update with Python-specific demo -->

## Features

- 🎙️ **Pre-Bundled Models**: Choose from different installer sizes (Tiny, Base, Small, Medium, Large)
- 🐍 **Python 3 Integration**: Designed for PyQt5/PySide2/Tkinter/Kivy etc.
- 🌍 **Auto-Detect Language**: Supports 100+ languages out of the box
- ⚡ **Hardware Acceleration**: CUDA/Metal support in dedicated installers
- 📦 **Self-Contained**: No Python dependencies required

## Installation

### For Subtl Users
1. Download the appropriate installer from [Releases](https://github.com/your-repo/releases):
   - `WhisperAI-Tiny.exe` (100MB) - Basic accuracy
   - `WhisperAI-Large.exe` (3GB) - Studio quality
2. Run the installer and follow platform-specific instructions
3. Launch Subtl - auto-detects available models in:
   ```bash
   # Windows
   %PROGRAMFILES%\SubtlExtensions\WhisperAI\

   # macOS
   /Applications/SubtlExtensions/WhisperAI/

   # Linux
   /opt/subtl-extensions/whisperai/
   ```

## IMPORTANT!!

Choose your model based on hardware capabilities and accuracy needs:

### Model Comparison Table
| Model Size | CPU Requirements          | RAM  | GPU Recommendation          | Disk Space | Processing Speed* | Best For                  |
|------------|---------------------------|------|------------------------------|------------|-------------------|---------------------------|
| **Tiny**   | Modern mobile processor   | 4GB+ | Integrated graphics          | 100MB      | 1× real-time      | Low-end PCs, Quick edits  |
| **Base**   | i5/Ryzen 5 (4-core)       | 6GB+ | Entry-level discrete GPU     | 500MB      | 4× faster         | General purpose use       |
| **Small**  | i7/Ryzen 7 (6-core)       | 8GB+ | GTX 1660/RTX 3050 (4GB VRAM) | 1GB        | 2× faster         | Content creators          |
| **Medium** | i9/Ryzen 9 (8-core)       | 12GB+| RTX 3060/RX 6700 (8GB VRAM)  | 2GB        | 1.5× faster       | Professional transcriptions |
| **Large**  | Xeon/Threadripper (12-core)| 16GB+| RTX 4080/RX 7900 (12GB VRAM) | 3GB        | 1×                | Studio-grade production   |

_*Speed relative to audio duration when using recommended GPU_

### Decision Guidelines

**Choose Tiny if:**
- Using a laptop without dedicated graphics
- Need instant results for short clips (<5 minutes)
- Have limited storage space

**Choose Base/Small if:**
- Typical desktop/laptop with gaming GPU
- Balance between speed and accuracy needed
- Processing videos under 30 minutes

**Choose Medium/Large if:**
- Have a high-end workstation with powerful GPU
- Need broadcast-quality subtitles
- Working with complex audio (multiple speakers, technical terms)

### Critical Requirements
- **GPU Users:** Requires compute capability 5.0+ (NVIDIA) or RDNA2+ (AMD)
- **Apple Silicon:** Medium/Large models require M1 Pro/Max/Ultra chips
- **Windows:** Needs DirectX 12 Ultimate for GPU acceleration
- **Linux:** Requires Vulkan 1.3 drivers for AMD GPUs

### Performance Tips
1. **RAM vs Model Size:** Your system RAM should be _at least 2×_ the model size
2. **VRAM Formula:** Minimum GPU memory = Model size × 1.5
   - Example: Large model (3GB) needs ≥4.5GB VRAM
3. **Batch Processing:** Add 2GB RAM overhead per concurrent transcription

### Verification Tools
Check your system capabilities:
- **Windows:** `dxdiag` in Start menu
- **macOS:** About This Mac > System Report
- **Linux:** `lspci -v | grep -i vga`
- **All Platforms:** Included `check_compatibility.exe` tool


## For Developers

### Basic Usage
```python
import subprocess
import json
from pathlib import Path

class WhisperAI:
    def __init__(self, model_size='base'):
        self.bin_path = Path(EXTENSION_PATHS[platform.system()]) / f'whisper-{model_size}'

    def transcribe(self, audio_path, output_format='srt'):
        cmd = [
            str(self.bin_path),
            '--input', str(audio_path),
            '--output', '-',  # Stdout output
            '--format', output_format
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            return self._parse_output(result.stdout, output_format)
        else:
            raise RuntimeError(f"Transcription failed: {result.stderr}")

    def _parse_output(self, output, format):
        # Implement parsing logic for JSON/SRT/VTT
        return output

# PyQt5 Example Integration
def generate_subtitles(parent_window):
    audio_file = parent_window.get_selected_media()
    whisper = WhisperAI(model_size='large')
    
    try:
        subs = whisper.transcribe(audio_file, format='srt')
        parent_window.import_subtitles(subs)
    except RuntimeError as e:
        show_error_dialog(str(e))
```

## Output Formats
Supported formats through `--format` parameter:
- JSON (default)
- SRT
- VTT
- TXT

Example SRT output:
```srt
1
00:00:00,000 --> 00:00:04,500
Welcome to today's conference call.

2
00:00:04,500 --> 00:00:08,200
Let's begin with Q1 financial results.
```

## Compatibility
- Requires Python 3.8+
- Officially tested with:
  - PyQt5 5.15+
  - PySide2 5.15+
  - Tkinter 8.6+
- Supported OS:
  - Windows 10+ (64-bit)
  - macOS 11+ (Apple Silicon/Intel)
  - Linux (Ubuntu 20.04+, Fedora 34+)

## Model Comparison
| Installer Size | VRAM Required | Relative Speed | Use Case |
|----------------|---------------|----------------|----------|
| Tiny (100MB)   | 1GB           | 32×            | Real-time |
| Base (500MB)   | 2GB           | 16×            | General purpose |
| Small (1GB)    | 4GB           | 8×             | High accuracy |
| Medium (2GB)   | 8GB           | 4×             | Professional |
| Large (3GB)    | 12GB          | 1×             | Studio quality |

## Contributing
Python developers welcome! To contribute:
1. Clone the repository
2. Use the bundler tool to package models:
   ```bash
   python bundler.py --model large --platform win64
   ```
3. Test with the included PyQt5 demo app
4. Submit PR with your improvements

## License
MIT License - See [LICENSE](LICENSE) for details

## Support
For Python integration help:
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Python Subprocess Guide](https://docs.python.org/3/library/subprocess.html)

