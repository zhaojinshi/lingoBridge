# lingoBridge Design QA

**Source visual truth**

- Light theme: `C:\Users\admin\.codex\generated_images\019f1b83-e316-7751-bb01-8bb1d7ec5b6c\exec-c12d358a-4402-449b-af55-062ae70e8b26.png`
- Dark theme: `C:\Users\admin\.codex\generated_images\019f1b83-e316-7751-bb01-8bb1d7ec5b6c\exec-3c34d831-7406-4b3b-9423-0d5978c7043b.png`

**Implementation screenshots**

- `C:\tmp\lingobridge-light-main.png`
- `C:\tmp\lingobridge-light-settings.png`
- `C:\tmp\lingobridge-dark-main.png`
- `C:\tmp\lingobridge-dark-settings.png`

**Viewport and state**

- Native PySide6 desktop UI rendered with Python 3.10 / PySide6 6.10.2.
- Main window shown in expanded translation-result state.
- Settings window shown on the AI model page.
- Both light and dark themes rendered with identical layout and content.

**Full-view comparison evidence**

- `C:\tmp\lingobridge-qa-light.png`
- `C:\tmp\lingobridge-qa-dark.png`
- The implementation keeps the selected concepts' compact expandable translator, restrained provider hierarchy, sidebar settings structure, blue glass-light palette, and graphite/teal dark palette.

**Focused region comparison evidence**

- Separate main-window and settings-window captures were inspected at original resolution. Additional crops were not needed because typography, controls, borders, and spacing were readable in the original captures.

**Required fidelity surfaces**

- Typography: Segoe UI / Microsoft YaHei hierarchy is consistent and readable in both themes.
- Spacing and layout: compact toolbar, result rhythm, settings sidebar, field spacing, radii, and elevation are consistent with the selected direction.
- Colors and tokens: light uses pearl-blue translucent surfaces and cobalt accents; dark uses graphite surfaces, teal primary accents, and amber Google-provider accents.
- Image and icon quality: native Qt standard icons are used in settings navigation; the main surface avoids placeholder artwork and legacy emoji branding.
- Copy and content: all existing lingoBridge labels and functional controls are preserved.

**Findings**

- No actionable P0, P1, or P2 findings remain.

**Patches made during QA**

- Removed low-contrast dark-theme volume icon.
- Added explicit dark-theme text color to the Settings control.
- Disabled the settings sidebar horizontal scrollbar.
- Removed the legacy brand icon from the main header.
- Added explicit theme-aware message-box text and button colors.
- Recolored native settings navigation icons for light and dark themes.

**Follow-up polish**

- [P3] A bespoke lingoBridge logo could replace the current text-only lockup in a later brand pass.
- [P3] Provider copy buttons shown in the concept were not added because they are not part of the existing functional scope.

**Final result**

final result: passed
