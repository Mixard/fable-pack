---
name: windows-desktop-e2e
description: Use when writing or debugging E2E tests for Windows native desktop apps (WPF, WinForms, Win32/MFC, Qt) with pywinauto and Windows UI Automation (UIA). Covers per-framework UIA reliability, testability setup, the pywinauto locator/wait/action API, Qt version-specific gotchas (QT_ACCESSIBILITY, Qt5/Qt6 window class names), screenshot fallback with DPI rules, and Job Object process containment.
---

# Windows Desktop E2E Testing

End-to-end testing for Windows native desktop apps using **pywinauto** backed by Windows UI Automation (UIA). Covers WPF, WinForms, Win32/MFC, and Qt (5.x / 6.x).

## When NOT to Use

- Web apps → use Playwright
- Electron / CEF / WebView2 → the HTML layer needs browser automation, not UIA
- Mobile → UIAutomator, XCUITest

## Core Concepts

All Windows desktop automation relies on **UI Automation (UIA)**, a Windows-built-in accessibility API. Every supported framework exposes a tree of UIA elements:

```
Your test (Python)
  └── pywinauto (UIA backend)
      └── Windows UI Automation API   ← built into Windows, framework-agnostic
          └── App's UIA provider      ← each framework ships its own
              └── Running .exe
```

**UIA quality by framework:**

| Framework | AutomationId source | Reliability | Notes |
|-----------|---------------------|-------------|-------|
| WPF | `x:Name` maps directly | Excellent | |
| WinForms | `AccessibleName` = AutomationId | Good | |
| UWP / WinUI 3 | native | Excellent | |
| Qt 6.x | native | Excellent | Accessibility on by default; class names are `Qt6*` |
| Qt 5.15+ | `objectName` / `accessibleName` | Good | Improved Accessibility module |
| Qt 5.7–5.14 | manual | Fair | Needs `QT_ACCESSIBILITY=1` |
| Win32 / MFC | control IDs | Fair | Text matching common |

## Setup

```bash
# Python 3.8+, Windows only
pip install pywinauto pytest pytest-html Pillow pytest-timeout
```

Verify UIA is reachable:

```python
from pywinauto import Desktop
Desktop(backend="uia").windows()  # lists all top-level windows
```

Install **Accessibility Insights for Windows** (free, Microsoft) to inspect the UIA element tree before writing tests.

## Testability Setup (by Framework)

The single most impactful thing is giving every interactive control a stable AutomationId before writing tests.

### WPF

```xml
<!-- XAML: x:Name becomes AutomationId automatically -->
<TextBox x:Name="usernameInput" />
<Button x:Name="btnLogin" Content="Login" />
```

### WinForms

```csharp
usernameInput.AccessibleName = "usernameInput";
btnLogin.AccessibleName = "btnLogin";
```

### Win32 / MFC

Control resource IDs in the `.rc` file are exposed as AutomationId strings (e.g. `IDC_EDIT_USERNAME` → AutomationId `"1001"`). Prefer `SetWindowText` for Name; add `IAccessible` for richer support.

## The pywinauto API — Locators, Waits, Actions

```python
import os, time
from pywinauto import Desktop

class BasePage:
    def __init__(self, window):
        self.window = window

    # --- Locators (priority order) ---
    def by_id(self, auto_id, **kw):
        """AutomationId — most stable. First choice."""
        return self.window.child_window(auto_id=auto_id, **kw)

    def by_name(self, name, **kw):
        """Visible text / accessible name."""
        return self.window.child_window(title=name, **kw)

    def by_class(self, cls, index=0, **kw):
        """Control class + index — fragile, avoid if possible."""
        return self.window.child_window(class_name=cls, found_index=index, **kw)

    # --- Waits ---
    def wait_visible(self, spec, timeout=10):
        spec.wait("visible", timeout=timeout)
        return spec

    def wait_gone(self, spec, timeout=10):
        spec.wait_not("visible", timeout=timeout)
        return spec

    def wait_window(self, title, timeout=10):
        """Wait for a new top-level window (dialogs, child windows)."""
        dlg = Desktop(backend="uia").window(title=title)
        dlg.wait("visible", timeout=timeout)
        return dlg

    def wait_until(self, fn, timeout=10, interval=0.3):
        """Poll an arbitrary condition — use when UIA events are unreliable."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                if fn():
                    return True
            except Exception:
                pass
            time.sleep(interval)
        raise TimeoutError(f"Condition not met within {timeout}s")

    # --- Actions ---
    def click(self, spec):
        self.wait_visible(spec)
        spec.click_input()

    def type_text(self, spec, text):
        self.wait_visible(spec)
        ctrl = spec.wrapper_object()
        try:
            ctrl.set_edit_text(text)
        except Exception:
            # Qt 5.x fallback: UIA Value Pattern may be incomplete
            import pywinauto.keyboard as kb
            ctrl.click_input()
            kb.send_keys("^a")
            kb.send_keys(text, with_spaces=True)

    def get_text(self, spec):
        ctrl = spec.wrapper_object()
        for attr in ("window_text", "get_value"):
            try:
                v = getattr(ctrl, attr)()
                if v:
                    return v
            except Exception:
                pass
        return ""

    def screenshot(self, name, artifact_dir="artifacts"):
        os.makedirs(artifact_dir, exist_ok=True)
        path = os.path.join(artifact_dir, f"{name}.png")
        self.window.capture_as_image().save(path)
        return path
```

**`wait("visible")` states:** pywinauto `wait`/`wait_not` accept `exists`, `visible`, `enabled`, `ready`, `active` (space-separated to combine).

### Locator Strategy

```
AutomationId  >  Name (text)  >  ClassName + index  >  XPath
  (stable)         (readable)       (fragile)           (last resort)
```

Inspect at runtime:

```python
win.print_control_identifiers()
win.child_window(auto_id="groupBox1").print_control_identifiers()
```

**Never use `time.sleep()` as primary synchronization** — use `wait()` or `wait_until()`.

## Launch Fixture (with filesystem isolation)

Launch via `subprocess.Popen` so you can pass an isolated environment, then connect pywinauto by PID. Note: on the pywinauto `Application` object use `wait_for_process_exit()`, not `wait_for_process()`.

```python
import os, subprocess, shlex, pytest
from pywinauto import Application

@pytest.fixture(scope="function")
def app(request, tmp_path):
    app_path  = os.environ["APP_PATH"]
    app_title = os.environ["APP_TITLE"]

    # Redirect all per-user storage to an isolated tmp directory
    env = os.environ.copy()
    env["QT_ACCESSIBILITY"] = "1"                       # required for Qt 5.x UIA
    env["APPDATA"]      = str(tmp_path / "AppData" / "Roaming")
    env["LOCALAPPDATA"] = str(tmp_path / "AppData" / "Local")
    env["TEMP"] = env["TMP"] = str(tmp_path / "Temp")
    for p in (env["APPDATA"], env["LOCALAPPDATA"], env["TEMP"]):
        os.makedirs(p, exist_ok=True)

    # shlex.split handles quoted args with spaces; plain split() breaks on them
    proc   = subprocess.Popen([app_path] + shlex.split(os.environ.get("APP_ARGS", "")), env=env)
    pw_app = Application(backend="uia").connect(process=proc.pid, timeout=15)
    win    = pw_app.window(title=app_title)
    win.wait("visible", timeout=15)
    yield win

    try:
        win.close()
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
    # tmp_path is cleaned up automatically by pytest

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, f"rep_{outcome.get_result().when}", outcome.get_result())
```

## Qt Specific

### Enable UIA in Qt 5.x

Qt 5.x accessibility is disabled by default in some builds (especially 5.7–5.14). Set the env var **before** launching. Qt 6.x enables accessibility by default — skip for Qt 6.

```python
os.environ["QT_ACCESSIBILITY"] = "1"
```

### Add Stable Identifiers to Qt Widgets

```cpp
// Set both objectName and accessibleName
void setTestId(QWidget* w, const char* id) {
    w->setObjectName(id);
    w->setAccessibleName(id);  // becomes UIA Name property
}
```

### Qt-Specific Quirks

**QComboBox** — the dropdown is a separate top-level window whose class varies by Qt version (`Qt5QWindowIcon` vs `Qt6QWindowIcon`):

```python
from pywinauto import Desktop

def select_combo_item(page, combo_spec, item_text):
    page.click(combo_spec)
    popup = Desktop(backend="uia").window(class_name_re="Qt[56]QWindowIcon")
    popup.wait("visible", timeout=5)
    popup.child_window(title=item_text).click_input()
```

**QMessageBox / QDialog** — also separate top-level windows:

```python
dlg = page.wait_window("Confirm")
dlg.child_window(title="OK").click_input()
```

**QTableWidget / QTableView** — row/cell access:

```python
table = page.by_id("tblUsers").wrapper_object()
cell  = table.cell(row=0, column=1)
print(cell.window_text())
```

**Self-drawn controls** (`paintEvent`-only, `QGraphicsView`, `QOpenGLWidget`) — UIA cannot see their internals; use the screenshot fallback below.

## Flaky Test Causes

| Cause | Fix |
|-------|-----|
| Control not ready | Replace `time.sleep` with `wait_visible` |
| Window not focused | Add `win.set_focus()` before interactions |
| Animation in progress | `wait_until(lambda: not loading_indicator.exists())` |
| Dialog timing | `wait_window(title, timeout=15)` |
| `set_edit_text` raises `NotImplementedError` | UIA ValuePattern missing (common on Qt 5.x) — fall back to `keyboard.send_keys` |
| Control exists but `wait_visible` times out | Window minimised/off-screen — call `win.restore()` + `win.set_focus()` first |

## Fallback: Screenshot Mode

When a control is not reachable via UIA (self-drawn, third-party, game engine):

```python
import pyautogui, cv2, numpy as np
from PIL import Image

def find_image_on_screen(template_path, confidence=0.85):
    screen   = np.array(pyautogui.screenshot())
    template = np.array(Image.open(template_path))
    result   = cv2.matchTemplate(
        cv2.cvtColor(screen, cv2.COLOR_RGB2BGR),
        cv2.cvtColor(template, cv2.COLOR_RGB2BGR),
        cv2.TM_CCOEFF_NORMED,
    )
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= confidence:
        h, w = template.shape[:2]
        return max_loc[0] + w // 2, max_loc[1] + h // 2
    return None
```

### DPI / Scaling Rules (screenshot mode only)

Screenshot matching is brutally sensitive to Windows display scaling (100% / 125% / 150%):

1. **Capture templates at the same scale as the target machine.** Don't rescue a mismatch with `PIL.Image.resize` — `cv2.matchTemplate` is fragile against resampling artefacts.
2. **Pin the CI display scaling** (e.g. `Set-DisplayResolution 1920 1080 -Force`) so screenshot dimensions are reproducible.
3. **Record the scale** — write `GetDpiForWindow(hwnd) / 96` alongside each artefact.

> Process-level DPI awareness (`SetProcessDpiAwarenessContext`) **can conflict with Qt's own DPI handling**. Prefer "same-scale templates + CI pin" over flipping process-wide DPI mode.

Always try UIA first; fall back to screenshots only for genuinely unreachable controls.

## Process Containment — Job Object

Attach the process to a Windows Job Object so it is automatically terminated when the fixture's job handle is GC'd (also prevents child-process escape). Job Objects do NOT virtualize filesystem or block network.

```python
import ctypes, ctypes.wintypes as wt

def restrict_process(pid: int):
    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
    PROCESS_SET_QUOTA_AND_TERMINATE    = 0x0101  # SET_QUOTA (0x0100) | TERMINATE (0x0001)

    kernel32 = ctypes.windll.kernel32
    job   = kernel32.CreateJobObjectW(None, None)
    hproc = kernel32.OpenProcess(PROCESS_SET_QUOTA_AND_TERMINATE, False, pid)

    class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", wt.LARGE_INTEGER),
            ("PerJobUserTimeLimit",     wt.LARGE_INTEGER),
            ("LimitFlags",              wt.DWORD),        # offset +16
            ("MinimumWorkingSetSize",   ctypes.c_size_t),
            ("MaximumWorkingSetSize",   ctypes.c_size_t),
            ("ActiveProcessLimit",      wt.DWORD),
            ("Affinity",                ctypes.c_size_t),
            ("PriorityClass",           wt.DWORD),
            ("SchedulingClass",         wt.DWORD),
        ]

    info = JOBOBJECT_BASIC_LIMIT_INFORMATION()
    info.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    if not kernel32.SetInformationJobObject(job, 2, ctypes.byref(info), ctypes.sizeof(info)):
        raise ctypes.WinError()
    kernel32.AssignProcessToJobObject(job, hproc)
    kernel32.CloseHandle(hproc)
    return job  # keep alive — job closes (kills proc) when GC'd
```

## CI/CD

Run on `windows-latest` — it is a real GUI environment, no Xvfb needed. Export `QT_ACCESSIBILITY: "1"` for Qt 5.x apps. Add `pytest-timeout` (`timeout = 60`, `timeout_method = thread`) to cap hanging tests; note the `thread` method cannot kill Qt subprocesses, so also reap orphans with `atexit`.

## Anti-Patterns

- Fixed `time.sleep()` instead of `wait_visible` / `wait_until`
- Brittle class+index locators as the primary strategy — use AutomationId
- Asserting on pixel coordinates (`btn.rectangle().left == 120`) instead of content/state (`is_enabled()`, `get_text()`)
- `scope="session"` app fixture (state leaks) — use `scope="function"` (per-class at most)
