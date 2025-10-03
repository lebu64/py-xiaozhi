# Voice Wake-up Function

## Overview

py-xiaozhi integrates high-precision voice wake-up function based on **Sherpa-ONNX**, supporting custom wake words and real-time detection. Uses lightweight keyword detection model, providing millisecond-level response speed.

## Wake Word Model

### Model Download (Required)

**Important Note**: The project does not include model files, need to download and configure in advance.

### Official Model Download Address

- **Official Model List**: <https://csukuangfj.github.io/sherpa/onnx/kws/pretrained_models/index.html>
- **Recommended Model**: `sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01`

### Download and Configuration Steps

#### 1. Download Model Package

```bash
# Method 1: Direct download (recommended)
cd /Users/junsen/Desktop/workspace/py-xiaozhi
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/kws-models/sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01.tar.bz2

# Extract
tar xvf sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01.tar.bz2

# Method 2: Use ModelScope
pip install modelscope
python -c "
from modelscope import snapshot_download
snapshot_download('pkufool/sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01', cache_dir='./models')
"
```

#### 2. Configure Model Files

The downloaded model package contains the following files:

```
sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01/
├── encoder-epoch-12-avg-2-chunk-16-left-64.int8.onnx    # Speed priority
├── encoder-epoch-12-avg-2-chunk-16-left-64.onnx         # 
├── encoder-epoch-99-avg-1-chunk-16-left-64.int8.onnx    # Speed priority 
├── encoder-epoch-99-avg-1-chunk-16-left-64.onnx         # Accuracy priority
├── decoder-epoch-12-avg-2-chunk-16-left-64.onnx         #
├── decoder-epoch-99-avg-1-chunk-16-left-64.onnx         # Accuracy priority
├── joiner-epoch-12-avg-2-chunk-16-left-64.int8.onnx     # Speed priority
├── joiner-epoch-12-avg-2-chunk-16-left-64.onnx          #
├── joiner-epoch-99-avg-1-chunk-16-left-64.int8.onnx     # Speed priority
├── joiner-epoch-99-avg-1-chunk-16-left-64.onnx          # Accuracy priority
├── tokens.txt                    # Token mapping table (required)
├── keywords_raw.txt              # Raw keywords (optional, for generation)
├── keywords.txt                  # Ready-made
├── test_wavs/                    # Test audio (optional)
├── configuration.json            # Model metadata (optional)
└── README.md                     # Documentation (optional)
```

#### 3. Select Configuration Scheme

**Scheme One: Accuracy Priority (Recommended)**

```bash
cd sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01

# Copy accuracy priority epoch-99 fp32 three files
cp encoder-epoch-99-avg-1-chunk-16-left-64.onnx ../models/encoder.onnx
cp decoder-epoch-99-avg-1-chunk-16-left-64.onnx ../models/decoder.onnx  
cp joiner-epoch-99-avg-1-chunk-16-left-64.onnx ../models/joiner.onnx

# Copy supporting files
cp tokens.txt ../models/tokens.txt
cp keywords_raw.txt ../models/keywords_raw.txt  # Optional
```

**Scheme Two: Speed Priority**

```bash
cd sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01

# Copy speed priority epoch-99 int8 three files
cp encoder-epoch-99-avg-1-chunk-16-left-64.int8.onnx ../models/encoder.onnx
cp decoder-epoch-99-avg-1-chunk-16-left-64.onnx ../models/decoder.onnx
cp joiner-epoch-99-avg-1-chunk-16-left-64.int8.onnx ../models/joiner.onnx

# Copy supporting files  
cp tokens.txt ../models/tokens.txt
```

**Notes**:

- **Do not mix fp32 and int8**: The three model files must maintain consistent precision
- **Prefer epoch-99**: More fully trained than epoch-12, higher accuracy
- **Required files**: `encoder.onnx` + `decoder.onnx` + `joiner.onnx` + `tokens.txt` + `keywords.txt`

### Final Model File Structure

After configuration, your models directory should contain:

```
models/
├── encoder.onnx      # Encoder model (after renaming)
├── decoder.onnx      # Decoder model (after renaming) 
├── joiner.onnx       # Joiner model (after renaming)
├── tokens.txt        # Pinyin Token mapping table (228 line version)
├── keywords.txt      # Keyword configuration file (need to create)
└── keywords_raw.txt  # Raw keyword file (optional)
```

### Model Performance Comparison

| Model Version | File Size | Inference Speed | Recognition Accuracy | Resource Usage | Recommended Scenario |
|--------------|-----------|----------------|---------------------|----------------|---------------------|
| **epoch-99 fp32** | ~13MB | Medium | Highest | Medium | **Desktop Computer (Recommended)** |
| **epoch-99 int8** | ~4MB | Fast | High | Low | Mobile Devices/Resource Constrained |
| **epoch-12 fp32** | ~13MB | Medium | Medium-High | Medium | General Use |
| **epoch-12 int8** | ~4MB | Fastest | Medium | Lowest | Extreme Speed Response Needs |

## Enable Voice Wake-up

### Configuration File Settings

Edit `config/config.json`:

```json
{
  "WAKE_WORD_OPTIONS": {
    "USE_WAKE_WORD": true,
    "MODEL_PATH": "models",
    "NUM_THREADS": 4,
    "PROVIDER": "cpu",
    "MAX_ACTIVE_PATHS": 2,
    "KEYWORDS_SCORE": 1.8,
    "KEYWORDS_THRESHOLD": 0.2,
    "NUM_TRAILING_BLANKS": 1
  }
}
```

### Configuration Parameter Details

| Parameter | Default Value | Description | Tuning Suggestions |
|-----------|---------------|-------------|-------------------|
| `USE_WAKE_WORD` | `true` | Enable voice wake-up function | - |
| `MODEL_PATH` | `"models"` | Model file directory | Ensure path is correct |
| `NUM_THREADS` | `4` | Processing thread count | Can set 6-8 if computer performance is good |
| `PROVIDER` | `"cpu"` | Inference engine | Options: cpu, cuda, coreml |
| `MAX_ACTIVE_PATHS` | `2` | Search path count | Reduce to improve speed, increase to improve accuracy |
| `KEYWORDS_SCORE` | `1.8` | Keyword enhancement score | Increase to reduce false detection, decrease to improve sensitivity |
| `KEYWORDS_THRESHOLD` | `0.2` | Detection threshold | Decrease to improve sensitivity, increase to reduce false detection |
| `NUM_TRAILING_BLANKS` | `1` | Trailing blank count | Usually keep at 1 |

## Custom Wake Words

### Currently Supported Wake Words

```
1. Xiao Ai Tong Xue    (x iǎo ài t óng x ué)
2. Ni Hao Wen Wen    (n ǐ h ǎo w èn w èn)
3. Xiao Yi Xiao Yi    (x iǎo y ì x iǎo y ì)
4. Xiao Mi Xiao Mi    (x iǎo m ǐ x iǎo m ǐ)
5. Ni Hao Xiao Zhi (n ǐ h ǎo x iǎo zh ì)
6. Jarvis (j iā w éi s ī)
```

### Add New Wake Words

#### Method 1: Edit Keyword File

Edit `models/keywords.txt`, add in format:

```
# Format: pinyin decomposition @Chinese original text
x iǎo zh ì @Xiao Zhi
n ǐ h ǎo x iǎo zh ì @Ni Hao Xiao Zhi
j iā w éi s ī @Jarvis
k āi sh ǐ g ōng z uò @Kai Shi Gong Zuo
```

#### Method 2: Use Pinyin Conversion Tool

```python
from pypinyin import lazy_pinyin, Style

def generate_keyword_line(text):
    pinyin_list = lazy_pinyin(text, style=Style.TONE3, neutral_tone_with_five=True)
    processed_pinyin = [py.rstrip('12345') for py in pinyin_list]
    pinyin_str = ' '.join(processed_pinyin)
    return f'{pinyin_str} @{text}'

# Generate new wake words
wake_words = ['Xiao Zhu Shou', 'Kai Shi Gong Zuo', 'Xing Qi Wu']
for word in wake_words:
    print(generate_keyword_line(word))
```

### Wake Word Selection Suggestions

#### Recommended Wake Word Characteristics

- **Moderate Length**: 2-4 characters
- **Clear Pronunciation**: Avoid similar sound confusion
- **Strong Uniqueness**: Avoid common daily conversation words
- **Easy to Remember**: Easy to memorize and pronounce

#### Example Good Wake Words

```
- Ni Hao Xiao Zhi    # 4 characters, unique, clear
- Jarvis             # 3 characters, unique, tech feel
- Kai Shi Gong Zuo   # 4 characters, clear intent
- Xiao Zhu Shou      # 3 characters, simple and easy to remember
```

#### Avoid Using

```
- En                # Too short, easy to trigger accidentally
- Ni Hao            # Too common
- Qing Bang Wo Zuo Yi Ge Ji Hua # Too long
- Xie Xie           # Daily language
```

## Usage Methods

### Startup Process

1. **Start Program**:

   ```bash
   cd /Users/junsen/Desktop/workspace/py-xiaozhi
   python main.py
   ```

2. **Model Loading**:
   - System automatically loads Sherpa-ONNX model
   - Initializes keyword detector
   - Enters wake word listening state

3. **Voice Wake-up**:
   - Clearly speak configured wake words
   - System automatically switches to LISTENING state
   - Starts voice conversation

### Usage Tips

#### Best Wake-up Methods

- **Moderate Volume**: Normal speaking volume
- **Natural Speed**: Not too fast or too slow
- **Clear Pronunciation**: Pay special attention to tones
- **Quiet Environment**: Reduce background noise

## Performance Optimization

### Speed Optimization Configuration

```json
{
  "WAKE_WORD_OPTIONS": {
    "NUM_THREADS": 6,           // Increase thread count
    "MAX_ACTIVE_PATHS": 1,      // Reduce search paths
    "KEYWORDS_THRESHOLD": 0.15, // Lower threshold to improve sensitivity
    "KEYWORDS_SCORE": 1.5       // Lower score to improve speed
  }
}
```

### Accuracy Optimization Configuration

```json
{
  "WAKE_WORD_OPTIONS": {
    "NUM_THREADS": 4,           // Moderate thread count
    "MAX_ACTIVE_PATHS": 3,      // Increase search paths
    "KEYWORDS_THRESHOLD": 0.25, // Increase threshold to reduce false detection
    "KEYWORDS_SCORE": 2.2       // Increase score to enhance accuracy
  }
}
```

### Performance Monitoring

Check current performance:

```python
# View statistical information in application
stats = wake_word_detector.get_performance_stats()
print(f"Engine: {stats['engine']}")
print(f"Thread Count: {stats['num_threads']}")
print(f"Detection Threshold: {stats['keywords_threshold']}")
print(f"Running Status: {stats['is_running']}")
```

## Troubleshooting

### Common Issues

#### 1. Wake Word No Response

**Symptoms**: Speaking wake word gets no response

**Solutions**:

```bash
# Check configuration
grep -A 10 "WAKE_WORD_OPTIONS" config/config.json

# Check model files
ls -la models/

# Test functionality
python test_new_keywords.py
```

#### 2. Slow Response Speed

**Symptoms**: Large wake word recognition delay

**Solutions**:

```json
{
  "WAKE_WORD_OPTIONS": {
    "KEYWORDS_THRESHOLD": 0.15,  // Lower threshold
    "NUM_THREADS": 6,            // Increase threads
    "MAX_ACTIVE_PATHS": 1        // Reduce search paths
  }
}
```

#### 3. Frequent False Detection

**Symptoms**: Often triggers wake-up incorrectly

**Solutions**:

```json
{
  "WAKE_WORD_OPTIONS": {
    "KEYWORDS_THRESHOLD": 0.3,   // Increase threshold
    "KEYWORDS_SCORE": 2.5,       // Increase score
    "MAX_ACTIVE_PATHS": 3        // Increase search paths
  }
}
```

#### 4. Model Loading Failure

**Symptoms**: Model file error when starting

**Solutions**:

```bash
# Check file integrity
ls -la models/
file models/*.onnx
file models/tokens.txt

# Re-verify model
python test_new_keywords.py
```

### Debug Commands

```bash
# View system logs
tail -f logs/app.log | grep -i kws

# Monitor performance
top -p $(pgrep -f "python main.py")

# Test audio devices
python -c "import sounddevice as sd; print(sd.query_devices())"
```

## Advanced Configuration

### Environment Adaptation

#### Quiet Environment (Office)

```json
{
  "WAKE_WORD_OPTIONS": {
    "KEYWORDS_THRESHOLD": 0.15,
    "KEYWORDS_SCORE": 1.5,
    "MAX_ACTIVE_PATHS": 1
  }
}
```

#### Noisy Environment (Open Space)

```json
{
  "WAKE_WORD_OPTIONS": {
    "KEYWORDS_THRESHOLD": 0.25,
    "KEYWORDS_SCORE": 2.5,
    "MAX_ACTIVE_PATHS": 3
  }
}
```

### Integration with AEC

Voice wake-up perfectly integrates with echo cancellation (AEC):

```json
{
  "AEC_OPTIONS": {
    "ENABLED": true,              // AEC provides clean audio for wake words
    "ENABLE_PREPROCESS": true     // Noise suppression improves detection accuracy
  },
  "WAKE_WORD_OPTIONS": {
    "USE_WAKE_WORD": true         // Use AEC processed audio
  }
}
```

### Performance Benchmarks

Expected performance under standard configuration:

| Metric | Target Value | Description |
|--------|--------------|-------------|
| **Response Latency** | < 1 second | From speaking to detection completion |
| **Detection Accuracy** | > 95% | Correctly recognizes set wake words |
| **False Detection Rate** | < 5% | Frequency of incorrect triggers |
| **CPU Usage** | < 30% | Resource consumption during continuous operation |
| **Memory Usage** | < 100MB | Model and buffer memory usage |

## Summary

**Sherpa-ONNX Voice Wake-up Function Features**:

- **High Accuracy**: End-to-end detection based on deep learning
- **Low Latency**: Millisecond-level response speed
- **Low Resource**: Lightweight model, suitable for PC operation
- **Customizable**: Supports custom wake words
- **Easy Integration**: Perfectly integrates with existing audio processing

Now you can enjoy intelligent, fast, and accurate voice wake-up experience!
