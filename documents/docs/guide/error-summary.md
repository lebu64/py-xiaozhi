# Error Problem Summary

## 1. `Could not find Opus library. Make sure it is installed.`

### **Error Description**

```
(.venv) C:\Users\Junsen\Desktop\learning\xiaozhi-python>python xiaozhi-python.py
Traceback (most recent call last):
  File "C:\Users\Junsen\Desktop\learning\xiaozhi-python\xiaozhi-python.py", line 5, in <module>
    import opuslib
  File "C:\Users\Junsen\Desktop\learning\xiaozhi-python\.venv\lib\site-packages\opuslib\__init__.py", line 19, in <module>
    from .exceptions import OpusError  # NOQA
  File "C:\Users\Junsen\Desktop\learning\xiaozhi-python\.venv\lib\site-packages\opuslib\exceptions.py", line 10, in <module>
    import opuslib.api.info
  File "C:\Users\Junsen\Desktop\learning\xiaozhi-python\.venv\lib\site-packages\opuslib\api\__init__.py", line 20, in <module>
    raise Exception(
Exception: Could not find Opus library. Make sure it is installed.
```

### **Solution**

1. **Windows**

   - Download and install Opus library.
   - Ensure `opuslib` related libraries correctly installed.

2. **Linux/macOS**

   - Run following commands to install `libopus`:
     ```sh
     sudo apt-get install libopus-dev  # Ubuntu/Debian
     brew install opus                 # macOS
     ```

3. **Python Code Installation**

   ```sh
   pip install opuslib
   ```

---

## 2. `externally-managed-environment` (macOS)

### **Error Description**

```
(.venv) huangjunsen@huangjunsendeMac-mini py-xiaozhi % pip install -r requirements_mac.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try brew install
    xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a Python library that isn't in Homebrew,
    use a virtual environment:
    
    python3 -m venv path/to/venv
    source path/to/venv/bin/activate
    python3 -m pip install xyz
    
    If you wish to install a Python application that isn't in Homebrew,
    it may be easiest to use 'pipx install xyz', which will manage a
    virtual environment for you. You can install pipx with
    
    brew install pipx
    
    You may restore the old behavior of pip by passing
    the '--break-system-packages' flag to pip, or by adding
    'break-system-packages = true' to your pip.conf file. The latter
    will permanently disable this error.
    
    If you disable this error, we STRONGLY recommend that you additionally
    pass the '--user' flag to pip, or set 'user = true' in your pip.conf
    file. Failure to do this can result in a broken Homebrew installation.
    
    Read more about this behavior here: <https://peps.python.org/pep-0668/>

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

### **Solution**

1. **Use Virtual Environment Installation**
   ```sh
   python3 -m venv my_env
   source my_env/bin/activate
   pip install -r requirements.txt
   ```
2. **Use **``** for Global Installation**
   ```sh
   brew install pipx
   pipx install package_name
   ```
3. **Force Installation (Not Recommended)**
   ```sh
   pip install package_name --break-system-packages
   ```

---

## 3. `WebSocket Connection Failed: BaseEventLoop.create_connection() got an unexpected keyword argument 'extra_headers'`

### **Error Description**

```python
# Establish WebSocket connection
self.websocket = await websockets.connect(
    self.WEBSOCKET_URL, 
    extra_headers=headers # In higher versions change to additional_headers=headers
)
```

### **Solution**

- **New Version **``: `extra_headers` changed to `additional_headers`.
- **Old Version **``: `additional_headers` changed to `extra_headers`.

---

## 4. `No Default Input/Output Audio Device Found`

### **Error Description**

```
AudioCodec - ERROR - Audio device initialization failed: [Errno -9996] Invalid input device (no default output device)
AudioCodec - WARNING - Unable to initialize audio device: [Errno -9996] Invalid input device (no default output device)
```

### **Solution**

1. **Windows**:

   - Enable microphone and speakers in **Sound Settings**.

2. **Linux/macOS**:

   ```sh
   pactl list sources | grep "Name"
   ```

3. **Check Available Audio Devices**:

   ```python
   import pyaudio
   p = pyaudio.PyAudio()
   for i in range(p.get_device_count()):
       print(f"Device {i}: {p.get_device_info_by_index(i)['name']}")
   ```

4. **Manually Specify Audio Device**:

   ```python
   stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, input_device_index=0)
   ```

---


## **5. `ModuleNotFoundError: No module named '_tkinter'` Common on Mac M4 and below ** 

### **Error Description**
```
(.venv) apple@appledeMac-mini py-xiaozhi % python main.py

Traceback (most recent call last):
  File "/Users/apple/Desktop/py-xiaozhi/main.py", line 5, in <module>
    from src.application import Application
  File "/Users/apple/Desktop/py-xiaozhi/src/application.py", line 23, in <module>
    from src.display import gui_display, cli_display
  File "/Users/apple/Desktop/py-xiaozhi/src/display/gui_display.py", line 2, in <module>
    import tkinter as tk
  File "/opt/homebrew/Cellar/python@3.12/3.12.9/Frameworks/Python.framework/Versions/3.12/lib/python3.12/tkinter/__init__.py", line 38, in <module>
    import _tkinter  # If this fails your Python may not be configured for Tk
    ^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named '_tkinter'
```

### **Solution**

1. **Install `tcl-tk`**
   ```sh
   brew upgrade tcl-tk # Usually first step is enough
   ```

2. **Check Homebrew `tcl-tk` Path**
   ```sh
   brew info tcl-tk
   ```

3. **Reinstall Python, and Link `tcl-tk`**
   ```sh
   brew install python-tk
   ```

4. **Manually Specify `Tcl/Tk` Path (If Necessary)**
   ```sh
   export PATH="/opt/homebrew/opt/tcl-tk/bin:$PATH"
   export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"
   export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"
   ```

5. **Recreate Virtual Environment**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

---

## 6. `Import opuslib Failed: No module named 'pyaudioop' or '_cffi_backend'`

### **Error Description**

```
Found opus library file: D:\xiaozhi\PC\py-xiaozhi-main\libs\windows\opus.dll
Added DLL search path: D:\xiaozhi\PC\py-xiaozhi-main\libs\windows
Successfully loaded opus.dll: D:\xiaozhi\PC\py-xiaozhi-main\libs\windows\opus.dll
Import opuslib failed: No module named 'pyaudioop'
Ensure opus dynamic library correctly installed or in correct location
```

or

```
Found opus library file: D:\xiaozhi\PC\py-xiaozhi-main\libs\windows\opus.dll
Added DLL search path: D:\xiaozhi\PC\py-xiaozhi-main\libs\windows
Successfully loaded opus.dll: D:\xiaozhi\PC\py-xiaozhi-main\libs\windows\opus.dll
Import opuslib failed: No module named '_cffi_backend'
Please ensure opus dynamic library correctly installed or in correct location
```

### **Solution**

1. **Python Version Compatibility Issue**
   - This error usually related to Python version, especially Python 3.13 version
   - Recommended to use Python 3.9-3.12 version

2. **Reinstall cffi**
   ```sh
   pip uninstall cffi
   pip install cffi
   ```

3. **opus.dll Placement**
   - Ensure opus.dll placed in correct locations (project root directory and System32 directory)
   ```sh
   # Check if copied to these locations
   C:\Windows\System32\opus.dll
   Project root directory\opus.dll
   Project root directory\libs\windows\opus.dll
   ```

4. **Install pyaudioop Support Library**
   - For 'pyaudioop' error, try downgrading Python version or installing related dependencies
   ```sh
   pip install pyaudio
   ```

---


## 8. `error: subprocess-exited-with-error` (Installing `numpy` Failed)

### **Error Description**
```
Collecting numpy==2.0.2 (from -r requirements.txt (line 8))
  Using cached https://mirrors.aliyun.com/pypi/packages/a9/75/10dd1f8116a8b796cb2c737b674e02d02e80454bda953fa7e65d8c12b016/numpy-2.0.2.tar.gz (18.9 MB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Installing backend dependencies ... done
  Preparing metadata (pyproject.toml) ... error
  error: subprocess-exited-with-error

  × Preparing metadata (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [21 lines of output]
      ...
      WARNING: Failed to activate VS environment: Could not parse vswhere.exe output
      ERROR: Unknown compiler(s): [['icl'], ['cl'], ['cc'], ['gcc'], ['clang'], ['clang-cl'], ['pgcc']]
      The following exception(s) were encountered:
      Running `icl ""` gave "[WinError 2] System cannot find specified file."
      Running `cl /?` gave "[WinError 2] System cannot find specified file."
      Running `cc --version` gave "[WinError 2] System cannot find specified file."
      Running `gcc --version` gave "[WinError 2] System cannot find specified file."
      Running `clang --version` gave "[WinError 2] System cannot find specified file."
      Running `clang-cl /?` gave "[WinError 2] System cannot find specified file."
      Running `pgcc --version` gave "[WinError 2] System cannot find specified file."

  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.

note: This is an issue with the package mentioned above, not pip.
hint: See above for details.
```

### **Solution**
- Recommended Python version 3.9 - 3.12

1. **Ensure `numpy` Version Compatibility**

   `numpy==2.0.2` may have build issues, recommended to try more stable version:
   ```sh
   pip install numpy==1.24.3
   ```

   If you don't need specific version, can install latest stable version:
   ```sh
   pip install numpy
   ```

2. **Install Compilation Tools**
   
   Windows users may need to install Visual C++ Build Tools:
   ```sh
   # Install Microsoft C++ Build Tools
   # Download and install: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   ```

3. **Use Pre-compiled Wheels**
   ```sh
   pip install --only-binary=numpy numpy
