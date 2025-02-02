# Subtl

![Subtl Logo](https://imgur.com/a/68ggd9i)

**Subtl** is a powerful desktop application designed to help you edit, change, and modify elements of your subtitles with ease. Whether you're a video editor, content creator, or just someone who loves watching movies with subtitles, Subtl provides a suite of tools to make subtitle editing a breeze.

For a comprehensive guide on how to use the app, including detailed instructions for each tool, please refer to the [Help Documentation](assets/modules/help.md).

## Features

- **Longer Appearance**: Extend the duration of your `.srt` subtitles to ensure they stay on screen longer.
- **Merge SRT**: Combine multiple `.srt` files into a single subtitle file.
- **Subtitle Converter**: Convert subtitles from any format to another format seamlessly.
- **Subtitle Shifter**: Shift subtitles either entirely or partially to sync them perfectly with your video.
- **Multilingual Merge**: Merge subtitles in different languages with optional color-coding for differentiation.

## Installation

### Windows
1. Download the latest release from the [Releases](https://github.com/yourusername/Subtl/releases) page.
2. Run the installer and follow the on-screen instructions.

### macOS
Installer coming soon, or you could use `pyinstaller` on your own:
1. Download source code.
2. Run the `.spec` file provided.

### Linux
Installer coming soon, or you could use `pyinstaller` on your own:
1. Download source code.
2. Run the `.spec` file provided.

## Usage

1. **Launch Subtl**: Open the application from your desktop or applications menu.
2. **Select a Tool**: Choose from the available tools in the main menu.
3. **Add New Tabs**: You can open several tools at the same time.
4. **Load Your Subtitle**: Import your subtitle file(s) into the app.
5. **Edit and Save**: Make the necessary changes and save your modified subtitle file.

### Navigating the Interface

- **Main Menu**: Displays tools you frequently use, recent tools, and all available tools.
- **Side Panel**: Provides quick access to additional features like settings and tabs. Toggle it using the menu button (`☰`) in the top-left corner.
- **Search Functionality**: Use the search bar at the top to quickly find tools by typing keywords related to the tool's name or description.

## Supported Subtitle Formats

Subtl supports a wide range of subtitle formats including:

- SubRip (`.srt`)
- MicroDVD (`.sub`)
- Plain Text (`.txt`)
- Advanced SubStation Alpha (`.ass`)
- SubStation Alpha (`.ssa`)
- WebVTT (`.vtt`)
- YouTube (`.sbv`)
- DFXP (`.dfxp`)
- Spruce Subtitle Format (`.stl`)
- VobSub (`.idx`)
- MPlayer (`.mpl`)
- Universal Subtitle Format (`.usf`)
- Lyric (`.lrc`)
- RealText (`.rt`)
- Timed Text Markup Language (`.ttml`)
- Captions (`.cap`)

**Note**: If you want to edit subtitles in formats other than `.srt` using tools like **Longer Appearance**, **Merge SRT**, or **Subtitle Shifter**, you must first convert them to `.srt` using the **Subtitle Converter** tool.

## Tools Overview

### Longer Appearance SRT
Extend the duration that each subtitle appears on the screen. Useful for fast-paced videos, accessibility enhancements, educational content, and live event subtitles.

### Merge SRT Files
Combine multiple subtitle files into one cohesive file. Offers two modes: **Glue End to End** (sequential merging) and **Stacked Merge** (parallel merging with optional color-coding).

### Subtitle Converter
Convert subtitles between different formats such as `.srt`, `.ass`, `.vtt`, `.sbv`, `.dfxp`, and more. Ideal for cross-platform compatibility and professional editing workflows.

### Subtitle Shifter
Shift subtitle timings by milliseconds. Offers two modes: **Whole Shift** (shift all subtitles uniformly) and **Partial Shift** (fine-tune specific sections).

### Multilingual Merge
Merge subtitles in different languages with optional color-coding for differentiation. Perfect for international films, corporate training, online courses, and travel vlogs.

## Settings

Access the settings via the side panel or the main menu:
- **Theme Selection**: Choose between light and dark modes.
- **Text Size Adjustment**: Customize the font size for better readability.
- **Reset Preferences**: Restore default settings if needed.

## Troubleshooting

If you encounter any issues, try the following:
1. **App Not Responding**: Close and relaunch the app. Ensure your system meets the minimum requirements.
2. **Missing Tools**: Verify that the tool is supported in your version of the app. Check for updates to access new features.
3. **Performance Issues**: Clear temporary files and restart your computer. Reduce the number of open tabs or windows.
4. **Search Not Working**: Ensure you're entering relevant keywords. Clear the search field and try again.

## Frequently Asked Questions (FAQ)

### Q: How do I merge subtitles in different languages?
A: Use the **Multilingual Merge** tool. Select the subtitle files for each language, assign unique colors for differentiation, and merge them into a single `.srt` file.

### Q: Can I convert subtitles to different formats?
A: Yes, use the **Subtitle Converter** tool. This tool supports converting between various subtitle formats such as `.srt`, `.ass`, `.vtt`, `.sbv`, `.dfxp`, and more.

### Q: Why are some tools grayed out or unavailable?
A: Some tools may be disabled if they require additional files or settings. For example:
- **Merge SRT Files**: Requires at least two `.srt` files to be selected.
- **Multilingual Merge**: Requires multiple `.srt` files in different languages.

### Q: How do I change the theme or text size?
A: You can customize the theme and text size in the **Settings** menu:
- **Change Theme**: Navigate to **Settings** > **Theme** and select your preferred theme (light or dark).
- **Adjust Text Size**: Go to **Settings** > **Text Size** and choose from options like "Small," "Default," "Large," or "Huge."

### Q: What should I do if the app crashes or becomes unresponsive?
A: Try the following steps:
1. Close and relaunch the app.
2. Ensure your system meets the minimum requirements for running the application.
3. Clear temporary files and restart your computer.
4. If the issue persists, report it via the GitHub repository or email support with details about the crash, including any error messages.

## Contributing

We welcome contributions from the community! If you'd like to contribute to Subtl, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

Please make sure to follow our [Code of Conduct](assets/CODE_OF_CONDUCT.md).

## License

Subtl is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Support

If you encounter any issues or have any questions, please open an issue on our [GitHub Issues](https://github.com/Liiesl/Subtl/issues) page.

## Acknowledgments

- Thanks to all the contributors who have helped make Subtl better.
- Special thanks to [Library/Technology Name] for making this project possible.

---

**Subtl** is developed with ❤️ by SubtlDevTeams (myself). Happy editing!
