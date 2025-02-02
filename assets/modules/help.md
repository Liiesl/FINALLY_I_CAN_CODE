# Subtl Help Guide

Welcome to **Subtl** help section! This guide will walk you through the features, navigation, and functionality of the application. Whether you're new to the app or looking for specific instructions, this document has you covered.

---

## Introduction

**Subtl** is a powerful tool designed to simplify subtitle management. With features like subtitle conversion, merging, shifting, and more, it caters to both beginners and advanced users. The app also offers customization options to tailor the experience to your preferences.

---

## Navigating the Interface

### Main Menu

The main menu is the central hub of the app. It includes:
- **Most Used Tools**: Displays tools you frequently use.
- **Recent Tools**: Shows tools you've accessed recently.
- **All Tools**: A comprehensive list of all available tools.

### Side Panel

The side panel provides quick access to additional features:
- Toggle it using the menu button (`☰`) in the top-left corner.
- Use it to navigate between tabs or access settings.

### Search Functionality

- Use the search bar at the top to quickly find tools.
- Type keywords related to the tool's name or description to filter results.

---

# Tools
**Subtl** offers a variety of powerful tools designed to streamline subtitle management. Whether you're adjusting timing, merging files, converting formats, or handling multilingual subtitles, these tools provide intuitive solutions for all your subtitle editing needs. Each tool is optimized for ease of use while maintaining precision and flexibility, ensuring that your subtitles are perfectly synchronized and formatted for any project.

## Disclaimer

All tools in **Subtl** are optimized to work with `.srt` subtitle files. If you have subtitles in other formats (e.g., `.ass`, `.vtt`, `.sub`, etc.), you can use the **Subtitle Converter** tool to convert them to

---

### Longer Appearance SRT

The **Longer Appearance SRT** tool allows you to extend the duration that each subtitle appears on the screen. This is useful when subtitles disappear too quickly, making them difficult to read.

### Use Cases:
- **Fast-Paced Videos**: Extend subtitle durations for action-packed scenes where viewers may struggle to read quickly disappearing text.
- **Accessibility Enhancements**: Make subtitles more accessible for viewers with reading difficulties by giving them extra time to process the text.
- **Educational Content**: Ensure students have ample time to read subtitles in educational videos without missing important information.
- **Live Event Subtitles**: Adjust subtitles for live performances or speeches where timing might not be perfectly aligned.

#### How to Use

1. **Access the Tool**:
   - From the main menu, locate the **Longer Appearance SRT** tool under "All Tools" or search for it using the search bar.
   - Click on the tool to open it.

2. **Select Subtitle Files**:
   - Once the tool is open, click the **Select Files** button.
   - A file dialog will appear. Choose one or more `.srt` subtitle files that you want to modify.
   - The selected files will be displayed in the list below the button.

3. **Adjust Duration**:
   - Use the dropdown menu labeled **Add Seconds** to specify how many seconds you want to add to the duration of each subtitle.
   - You can choose between 1 and 5 seconds.

4. **Export Modified Files**:
   - After adjusting the duration, click the **Export** button.
   - A save dialog will appear, allowing you to choose where to save the modified subtitle files.
   - The tool will automatically adjust the stop time of each subtitle by the number of seconds you specified and save the updated `.srt` file.

#### Example Workflow

1. Open the **Longer Appearance SRT** tool.
2. Select your `.srt` files using the **Select Files** button.
3. Choose **3 seconds** from the dropdown menu.
4. Click **Export** and save the modified files to your desired location.

#### Notes

- If no files are selected, an error message will appear prompting you to select files before exporting.
- The tool processes each file individually and saves the modified version with a prefix (e.g., `modified_filename.srt`).
- If any file fails to process, an error message will be displayed, but other files will continue to be processed.

---

### Merge SRT Files

The **Merge SRT Files** tool allows you to combine multiple subtitle files into one cohesive file. It offers two modes: **Glue End to End** and **Stacked Merge**.

### Use Cases:
- **Episodic Content**: Combine subtitles from multiple episodes into a single file for binge-watchers who prefer continuous playback.
- **Multilingual Presentations**: Create a unified subtitle file for presentations delivered in different languages during international conferences.
- **Film Festivals**: Prepare a single subtitle file for films shown back-to-back at festivals, ensuring seamless transitions between segments.
- **YouTube Playlists**: Merge subtitles for videos in a playlist so that viewers can watch the entire series without interruptions.

#### Modes

1. **Glue End to End**:
   - Combines subtitles sequentially, appending one after another.
   - Useful when you want to merge subtitles from different parts of a video.

2. **Stacked Merge**:
   - Combines subtitles in parallel, allowing for multilingual subtitles with optional color-coding.
   - Ideal for creating subtitles in multiple languages that appear simultaneously.

#### How to Use

1. **Access the Tool**:
   - From the main menu, locate the **Merge SRT Files** tool under "All Tools" or search for it using the search bar.
   - Click on the tool to open it.

2. **Select Mode**:
   - The tool provides two merging modes:
     - **Glue End to End**: Combines subtitles sequentially, appending one after another.
     - **Stacked Merge**: Combines subtitles in parallel, allowing for multilingual subtitles with optional color-coding.

   - Choose the mode by clicking either the **Glue End to End** or **Stacked Merge** button.

3. **Glue End to End Mode**:
   - **Select Main Subtitle**: Click the **Select Main Subtitle** button and choose the primary `.srt` file.
   - **Select Secondary Subtitle**: Click the **Select Secondary Subtitle** button and choose the secondary `.srt` file.
   - **Base Length**: Enter the length of the main subtitle's video in `hh:mm:ss` format.
   - **Export**: Click the **Export** button to merge the files and save the result.

4. **Stacked Merge Mode**:
   - **Select Main Subtitle**: Click the **Select Main Subtitle** button and choose the primary `.srt` file.
   - **Select Secondary Subtitles**: Click the **Select Secondary Subtitles** button and choose multiple `.srt` files.
   - **Color Options**: Toggle the color option to enable color-coding for merged subtitles. You can select a color from the dropdown or enter a custom hex code.
   - **Export**: Click the **Export** button to merge the files and save the result.

#### Example Workflow

1. Open the **Merge SRT Files** tool.
2. Select **Glue End to End** mode.
3. Choose the main subtitle file and the secondary subtitle file.
4. Enter the base length of the main subtitle's video (e.g., `01:30:00`).
5. Click **Export** and save the merged file.

Alternatively, for **Stacked Merge**:

1. Open the **Merge SRT Files** tool.
2. Select **Stacked Merge** mode.
3. Choose the main subtitle file and multiple secondary subtitle files.
4. Enable color-coding and select a color.
5. Click **Export** and save the merged file.

#### Notes

- Ensure that the base length is entered correctly in `hh:mm:ss` format for **Glue End to End** mode.
- For **Stacked Merge**, you can merge subtitles in different languages and optionally color-code them for differentiation.
- If any file fails to process, an error message will be displayed, but other files will continue to be processed.

---

### Subtitle Converter

The **Subtitle Converter** tool allows you to convert subtitles between different formats. Supported formats include `.srt`, `.ass`, `.sub`, `.vtt`, `.sbv`, `.dfxp`, `.stl`, `.mpl`, `.usf`, `.lrc`, `.rt`, `.ttml`, and `.cap`.

### Use Cases:
- **Cross-Platform Compatibility**: Convert `.srt` files to `.vtt` for web-based video players like YouTube or Vimeo.
- **Legacy Systems**: Transform older subtitle formats (e.g., `.sub`) into modern formats (e.g., `.ass`) for compatibility with current software.
- **Professional Editing**: Convert subtitles to `.dfxp` for use in professional video editing suites like Adobe Premiere Pro.
- **Mobile Devices**: Change subtitle formats to `.sbv` for better compatibility with Android devices or specific media players.

#### How to Use

1. **Access the Tool**:
   - From the main menu, locate the **Subtitle Converter** tool under "All Tools" or search for it using the search bar.
   - Click on the tool to open it.

2. **Select Subtitle Files**:
   - Click the **Select File** button and choose one or more subtitle files you want to convert.
   - The selected files will be displayed in the list below the button.

3. **Choose Target Format**:
   - Use the dropdown menu labeled **Select Source Format** to choose the format you want to convert the subtitles to.
   - Supported formats include `.srt`, `.ass`, `.sub`, `.vtt`, `.sbv`, `.dfxp`, `.stl`, `.mpl`, `.usf`, `.lrc`, `.rt`, `.ttml`, and `.cap`.

4. **Convert Files**:
   - After selecting the target format, click the **Convert** button.
   - A save dialog will appear, allowing you to choose where to save the converted subtitle files.
   - The tool will convert the subtitles to the selected format and save the updated files.

#### Example Workflow

1. Open the **Subtitle Converter** tool.
2. Select your subtitle files using the **Select File** button.
3. Choose the target format (e.g., `.vtt`) from the dropdown menu.
4. Click **Convert** and save the converted files to your desired location.

#### Notes

- If no files are selected, an error message will appear prompting you to select files before converting.
- The tool processes each file individually and saves the converted version with the appropriate file extension.
- If any file fails to process, an error message will be displayed, but other files will continue to be processed.

---

### Subtitle Shifter

The **Subtitle Shifter** tool allows you to shift subtitle timings by milliseconds. It offers two modes: **Whole Shift** and **Partial Shift**.

### Use Cases:
- **Audio Sync Issues**: Fix out-of-sync subtitles caused by audio delays in poorly encoded videos.
- **Editing Workflow**: Adjust subtitle timings during post-production when scene lengths are modified.
- **Time Zone Differences**: Shift subtitles to match localized broadcast times for global audiences.
- **Interactive Media**: Fine-tune subtitle timings for interactive media, such as video games or VR experiences, where user actions affect playback speed.

#### Modes

1. **Whole Shift**:
   - Shifts the timing of all subtitles by a specified number of milliseconds.
   - Useful for synchronizing subtitles with video playback.

2. **Partial Shift**:
   - Shifts the timing of subtitles within a specific time range.
   - Ideal for fine-tuning specific sections of subtitles.

#### How to Use

1. **Access the Tool**:
   - From the main menu, locate the **Subtitle Shifter** tool under "All Tools" or search for it using the search bar.
   - Click on the tool to open it.

2. **Select Mode**:
   - The tool provides two shifting modes:
     - **Whole Shift**: Shifts the timing of all subtitles by a specified number of milliseconds.
     - **Partial Shift**: Shifts the timing of subtitles within a specific time range.

   - Choose the mode by clicking either the **Whole Shift** or **Partial Shift** button.

3. **Whole Shift Mode**:
   - **Select Subtitle File**: Click the **Select Subtitle File** button and choose the `.srt` file you want to modify.
   - **Shift by (milliseconds)**: Enter the number of milliseconds you want to shift the subtitles by.
   - **Shift**: Click the **Shift** button to apply the changes and save the modified file.

4. **Partial Shift Mode**:
   - **Select Subtitle File**: Click the **Select Subtitle File** button and choose the `.srt` file you want to modify.
   - **Start Time**: Enter the start time of the section you want to shift (in `hh:mm:ss,fff` format).
   - **End Time**: Enter the end time of the section you want to shift (in `hh:mm:ss,fff` format).
   - **Shift by (milliseconds)**: Enter the number of milliseconds you want to shift the subtitles by.
   - **Shift**: Click the **Shift** button to apply the changes and save the modified file.

#### Example Workflow

1. Open the **Subtitle Shifter** tool.
2. Select **Whole Shift** mode.
3. Choose the `.srt` file you want to modify.
4. Enter **1000 milliseconds** in the "Shift by" field.
5. Click **Shift** and save the modified file.

Alternatively, for **Partial Shift**:

1. Open the **Subtitle Shifter** tool.
2. Select **Partial Shift** mode.
3. Choose the `.srt` file you want to modify.
4. Enter the **start time** (`00:01:00,000`) and **end time** (`00:02:00,000`) of the section you want to shift.
5. Enter **500 milliseconds** in the "Shift by" field.
6. Click **Shift** and save the modified file.

#### Notes

- Ensure that the start and end times are entered correctly in `hh:mm:ss,fff` format for **Partial Shift** mode.
- If any file fails to process, an error message will be displayed, but other files will continue to be processed.

---

### Multilingual Merge

The **Multilingual Merge** tool allows you to merge subtitles in different languages with optional color-coding for differentiation.

### Use Cases:
- **International Films**: Combine subtitles in multiple languages for foreign films, allowing viewers to choose their preferred language.
- **Corporate Training**: Provide multilingual subtitles for training videos used across global offices.
- **Online Courses**: Offer subtitles in various languages for e-learning platforms catering to diverse student populations.
- **Travel Vlogs**: Add subtitles in multiple languages for travel vlogs aimed at international audiences.

#### How to Use

1. **Access the Tool**:
   - From the main menu, locate the **Multilingual Merge** tool under "All Tools" or search for it using the search bar.
   - Click on the tool to open it.

2. **Select Subtitles**:
   - Click the **Select Subtitles** button and choose multiple `.srt` files, each containing subtitles in a different language.

3. **Assign Colors**:
   - Double-click on a subtitle file in the list to assign a color for that language.
   - A color picker will appear, allowing you to select a color for differentiation.

4. **Export Merged File**:
   - After assigning colors, click the **Export** button.
   - A save dialog will appear, allowing you to choose where to save the merged subtitle file.
   - The tool will combine the subtitles into a single `.srt` file with color-coded differentiation.

#### Example Workflow

1. Open the **Multilingual Merge** tool.
2. Select multiple `.srt` files, each containing subtitles in a different language.
3. Double-click on each file in the list and assign a unique color for differentiation.
4. Click **Export** and save the merged file to your desired location.

#### Notes

- The tool supports multiple languages and allows for color-coded differentiation to make multilingual subtitles easier to read.
- If any file fails to process, an error message will be displayed, but other files will continue to be processed.

---

## Settings

Access the settings via the side panel or the main menu:
- **Theme Selection**: Choose between light and dark modes.
- **Text Size Adjustment**: Customize the font size for better readability.
- **Reset Preferences**: Restore default settings if needed.

---

## Troubleshooting

If you encounter any issues, try the following:

1. **App Not Responding**:
   - Close and relaunch the app.
   - Ensure your system meets the minimum requirements.

2. **Missing Tools**:
   - Verify that the tool is supported in your version of the app.
   - Check for updates to access new features.

3. **Performance Issues**:
   - Clear temporary files and restart your computer.
   - Reduce the number of open tabs or windows.

4. **Search Not Working**:
   - Ensure you're entering relevant keywords.
   - Clear the search field and try again.

---

## Frequently Asked Questions (FAQ)

### Q: How do I merge subtitles in different languages?
A: Use the **Multilingual Merge** tool. Select the subtitle files for each language, assign unique colors for differentiation, and merge them into a single `.srt` file.  
- **Steps**:  
  1. Open the **Multilingual Merge** tool.  
  2. Click **Select Subtitles** and choose multiple `.srt` files, each containing subtitles in a different language.  
  3. Double-click on each file in the list to assign a color for that language using the color picker.  
  4. Click **Export** to save the merged file with color-coded subtitles.

---

### Q: Can I convert subtitles to different formats?
A: Yes, use the **Subtitle Converter** tool. This tool supports converting between various subtitle formats such as `.srt`, `.ass`, `.vtt`, `.sbv`, `.dfxp`, and more.  
- **Steps**:  
  1. Open the **Subtitle Converter** tool.  
  2. Select the subtitle files you want to convert.  
  3. Choose the target format from the dropdown menu.  
  4. Click **Convert** and save the converted files to your desired location.

---

### Q: Why are some tools grayed out or unavailable?
A: Some tools may be disabled if they require additional files or settings. For example:
- **Merge SRT Files**: Requires at least two `.srt` files to be selected.  
- **Multilingual Merge**: Requires multiple `.srt` files in different languages.  
- **Coming Soon Tools**: These are placeholders for future features and are not yet functional.

---

### Q: How do I change the theme or text size?
A: You can customize the theme and text size in the **Settings** menu:
- **Change Theme**:  
  1. Open the side panel by clicking the menu button (`☰`).  
  2. Navigate to **Settings** > **Theme** and select your preferred theme (light or dark).  
- **Adjust Text Size**:  
  1. Go to **Settings** > **Text Size**.  
  2. Choose from options like "Small," "Default," "Large," or "Huge."  

The app will automatically apply your changes.

---

### Q: What should I do if the app crashes or becomes unresponsive?
A: Try the following steps:
1. Close and relaunch the app.  
2. Ensure your system meets the minimum requirements for running the application.  
3. Clear temporary files and restart your computer.  
4. If the issue persists, report it via the GitHub repository or email support with details about the crash, including any error messages.

---

### Q: How do I search for specific tools?
A: Use the search bar at the top of the main menu:
- Type keywords related to the tool's name or description (e.g., "merge," "convert," "shift").  
- The search results will dynamically filter the available tools.  
- If no results appear, ensure you're entering relevant keywords or clear the search field and try again.

---

### Q: Why are my subtitles still out of sync after using the Subtitle Shifter?
A: Ensure you're entering the correct timing adjustments:
- **Whole Shift Mode**: Enter the number of milliseconds to shift all subtitles uniformly.  
- **Partial Shift Mode**: Specify the start and end times in `hh:mm:ss,fff` format and the number of milliseconds to shift within that range.  
If the issue persists, double-check the original subtitle file for inconsistencies or errors.

---

### Q: How do I access the side panel?
A: The side panel provides quick access to additional features:
- Click the menu button (`☰`) in the top-left corner to toggle the side panel.  
- Alternatively, use the keyboard shortcut `Ctrl + M` (if implemented).  
- The side panel can also be accessed via the **Custom Window Bar** or **Notification Bar**.

---

### Q: What are the most used tools, and how are they determined?
A: The **Most Used Tools** section displays tools you frequently use, based on usage statistics:
- The app tracks how often you use each tool and displays the top three most used tools in this section.  
- If no usage data is available, this section will remain hidden.

---

### Q: How do I report bugs or suggest new features?
A: As this project is maintained by a solo developer, you can report bugs or suggest features via the following channels:
- **GitHub Repository**: Visit the [Subtl GitHub Page](https://github.com/yourusername/subtl) to open an issue or submit a pull request.  
- **Email**: Send an email to **your.email@example.com** with details about the bug or feature request.  
- **Discussions**: Join the conversation in the [GitHub Discussions](https://github.com/yourusername/subtl/discussions) section to share ideas and feedback.

---

### Q: How do I handle subtitles in unsupported formats?
A: Use the **Subtitle Converter** tool to convert unsupported formats (e.g., `.ass`, `.vtt`) into `.srt` files before using other tools. Supported formats include `.srt`, `.ass`, `.sub`, `.vtt`, `.sbv`, `.dfxp`, `.stl`, `.mpl`, `.usf`, `.lrc`, `.rt`, `.ttml`, and `.cap`.

---

### Q: What happens if a tool fails to process a file?
A: If a tool encounters an issue while processing a file:
- An error message will be displayed, indicating the problematic file.  
- Other files in the queue will continue to be processed.  
- Check the file for formatting issues or inconsistencies and try again.

---

### Q: How do I view the changelog or check for updates?
A: Access the changelog through the side panel:
- Click the menu button (`☰`) to open the side panel.  
- Select **Changelog** from the list to view recent updates and changes.  
Alternatively, visit the official GitHub repository for the latest version history.

---

### Q: Can I customize the appearance of the app further?
A: While the app currently supports light and dark themes, as well as text size adjustments, further customization options may be added in future updates. Stay tuned to the GitHub repository for announcements.

---

### Q: How do I contact the developer directly?
A: As a solo developer, I appreciate direct feedback and inquiries. You can reach me via:
- **GitHub**: Open an issue or discussion on the [Subtl GitHub Page](https://github.com/yourusername/subtl).  
- **Email**: Send an email to **your.email@example.com** with your query.  
- **Social Media**: Connect with me on platforms like Instagram (@suryaalingga) or YouTube (@Vfrix) for informal communication.

---

## Contact Support

For further assistance, please reach out via the following channels:

- **GitHub Repository**: Visit the [Subtl GitHub Page](https://github.com/yourusername/subtl) to report issues, request features, or ask questions.  
- **Email**: You can also email me directly at **your.email@example.com** for more personalized support.
- **Discussions**: Join the conversation in the [GitHub Discussions](https://github.com/yourusername/subtl/discussions) section to connect with other users and share ideas.

As this project is maintained by a single developer, I appreciate your patience and understanding. Please include as much detail as possible when reporting issues (e.g., error messages, steps to reproduce).  

I aim to respond within 24–48 hours, but response times may vary depending on workload. Thank you for your support and for using **Subtl**!

---

Thank you for using **Subtl**! We hope this guide helps you make the most of the app. For updates and new features, stay tuned to our official website.

---
