# Music Tools

Music Tools is a feature-rich MCP music player that supports online search and playback, local music management, lyrics display, and other functions.

### Common Usage Scenarios

**Search and Play Online Music:**
- "Play Jay Chou's Blue and White Porcelain"
- "I want to listen to G.E.M.'s songs"
- "Play some light music"
- "Play the latest pop songs"

**Playback Control:**
- "Pause music"
- "Continue playback"
- "Stop playback"
- "Music is halfway through"

**Local Music Management:**
- "View local music"
- "Play that song from local"
- "Search for Jay Chou in local music"

**Playback Status Query:**
- "What song is playing now"
- "How's the playback progress"
- "How much time is left for this song"

**Lyrics Function:**
- "Show lyrics"
- "What are the current lyrics"
- "Are there lyrics available"

**Advanced Functions:**
- "Jump to 1 minute 30 seconds"
- "Fast forward to the climax part"
- "Go back to the beginning"

### Usage Tips

1. **Clear Song Information**: Providing song name, artist name, or album name helps with more accurate searches
2. **Network Connection**: Online search and playback require stable network connection
3. **Local Cache**: Played songs are automatically cached for faster playback next time
4. **Volume Control**: You can request volume adjustment or mute
5. **Lyrics Synchronization**: Supports real-time lyrics display to enhance listening experience

The AI assistant will automatically call the music tools based on your needs and provide you with a smooth music experience.

## Feature Overview

### Online Music Function
- **Smart Search**: Supports various search methods including song name, artist, album, etc.
- **High-Quality Playback**: Supports high-quality audio stream playback
- **Lyrics Display**: Real-time synchronized lyrics display
- **Automatic Cache**: Played songs are automatically cached locally

### Local Music Management
- **Local Scanning**: Automatically scans local music files
- **Metadata Extraction**: Automatically extracts song title, artist, album, and other information
- **Format Support**: Supports multiple formats including MP3, M4A, FLAC, WAV, OGG, etc.
- **Smart Search**: Quick search within local music

### Playback Control Function
- **Basic Control**: Play, pause, stop
- **Progress Control**: Jump to specified time position
- **Status Query**: Get playback status, progress, and other information
- **Error Handling**: Comprehensive error handling and recovery mechanism

### User Experience Function
- **UI Integration**: Seamlessly integrates with application interface
- **Real-time Feedback**: Real-time display of playback status and lyrics
- **Smart Cache**: Optimizes storage space usage
- **Background Playback**: Supports continuous background playback

## Tool List

### 1. Online Music Tools

#### search_and_play - Search and Play
Search online music and start playback.

**Parameters:**
- `song_name` (required): Song name, artist, or keywords to search

**Usage Scenarios:**
- Play specified song
- Search artist's songs
- Play popular music

### 2. Local Music Tools

#### get_local_playlist - Get Local Music List
Get list of locally cached music files.

**Parameters:**
- `force_refresh` (optional): Whether to force refresh, default false

**Usage Scenarios:**
- View local music
- Manage music library
- Select playlist

#### search_local_music - Search Local Music
Search for specified song in local music.

**Parameters:**
- `query` (required): Search keywords

**Usage Scenarios:**
- Find local songs
- Artist search
- Album search

#### play_local_song_by_id - Play Local Song
Play local music based on song ID.

**Parameters:**
- `file_id` (required): Local music file ID

**Usage Scenarios:**
- Play specified local song
- Select from playlist
- Quick playback of cached music

### 3. Playback Control Tools

#### play_pause - Play/Pause Toggle
Toggle between play and pause states.

**Parameters:**
None

**Usage Scenarios:**
- Pause current playback
- Resume playback
- Playback control

#### stop - Stop Playback
Stop current playback.

**Parameters:**
None

**Usage Scenarios:**
- Completely stop playback
- End music session
- Clear playback status

#### seek - Jump to Specified Position
Jump to specified time position in song.

**Parameters:**
- `position` (required): Jump position (seconds)

**Usage Scenarios:**
- Fast forward to climax part
- Repeat certain section
- Skip disliked parts

### 4. Information Query Tools

#### get_status - Get Playback Status
Get detailed status information of current player.

**Parameters:**
None

**Usage Scenarios:**
- View playback progress
- Check playback status
- Get song information

#### get_lyrics - Get Lyrics
Get lyrics of currently playing song.

**Parameters:**
None

**Usage Scenarios:**
- Display lyrics
- Sing along with song
- Learn lyrics

## Usage Examples

### Online Music Playback Examples

```python
# Search and play song
result = await mcp_server.call_tool("search_and_play", {
    "song_name": "Jay Chou Blue and White Porcelain"
})

# Play/pause control
result = await mcp_server.call_tool("play_pause", {})

# Stop playback
result = await mcp_server.call_tool("stop", {})

# Jump to specified position
result = await mcp_server.call_tool("seek", {
    "position": 90.5
})
```

### Local Music Management Examples

```python
# Get local music list
result = await mcp_server.call_tool("get_local_playlist", {
    "force_refresh": True
})

# Search local music
result = await mcp_server.call_tool("search_local_music", {
    "query": "Jay Chou"
})

# Play local song
result = await mcp_server.call_tool("play_local_song_by_id", {
    "file_id": "song_123"
})
```

### Status Query Examples

```python
# Get playback status
result = await mcp_server.call_tool("get_status", {})

# Get lyrics
result = await mcp_server.call_tool("get_lyrics", {})
```

## Technical Architecture

### Music Player Core
- **Singleton Pattern**: Globally unique player instance
- **Asynchronous Design**: Supports asynchronous operations without blocking main thread
- **State Management**: Comprehensive playback state management
- **Error Handling**: Robust error handling mechanism

### Audio Processing
- **Pygame Integration**: Uses Pygame Mixer for audio playback
- **Format Support**: Supports multiple audio formats
- **Cache Mechanism**: Smart caching strategy to reduce repeated downloads
- **Sound Quality Optimization**: High-quality audio playback

### Online Service Integration
- **API Interface**: Integrated online music search API
- **Download Management**: Asynchronous download and cache management
- **Lyrics Service**: Real-time lyrics acquisition and display
- **Network Optimization**: Network request optimization and retry mechanism

### Local Music Management
- **File Scanning**: Automatically scans local music files
- **Metadata Extraction**: Uses Mutagen library to extract music metadata
- **Index Building**: Builds music file index to improve search efficiency
- **Format Recognition**: Intelligent recognition of music file formats

## Data Structure

### Playback Status Information
```python
{
    "status": "success",
    "current_song": "Blue and White Porcelain - Jay Chou",
    "is_playing": true,
    "paused": false,
    "duration": 237.5,
    "position": 89.2,
    "progress": 37.6,
    "has_lyrics": true
}
```

### Music Metadata
```python
{
    "file_id": "song_123",
    "title": "Blue and White Porcelain",
    "artist": "Jay Chou",
    "album": "I'm Busy",
    "duration": "03:57",
    "file_size": 5242880,
    "format": "mp3"
}
```

### Lyrics Data
```python
{
    "status": "success",
    "lyrics": [
        "[00:12] Plain embryo outlines blue and white brush strokes turning from thick to light",
        "[00:18] The peony painted on the vase is like your first makeup",
        "[00:24] Rising sandalwood fragrance through the window, I understand your thoughts"
    ]
}
```

## Configuration Description

### Audio Configuration
Audio playback related configuration:
```python
AudioConfig = {
    "OUTPUT_SAMPLE_RATE": 44100,
    "CHANNELS": 2,
    "BUFFER_SIZE": 1024
}
```

### Cache Configuration
Cache directory configuration:
```python
cache_dir = Path(project_root) / "cache" / "music"
temp_cache_dir = cache_dir / "temp"
```

### API Configuration
Online music service configuration:
```python
config = {
    "SEARCH_URL": "http://search.kuwo.cn/r.s",
    "PLAY_URL": "http://api.xiaodaokg.com/kuwo.php",
    "LYRIC_URL": "http://m.kuwo.cn/newh5/singles/songinfoandlrc"
}
```

## Supported Audio Formats

### Playback Formats
- **MP3**: Most common audio format
- **M4A**: Apple audio format
- **FLAC**: Lossless audio format
- **WAV**: Uncompressed audio format
- **OGG**: Open source audio format

### Metadata Support
- **ID3 v1/v2**: MP3 metadata standard
- **MP4**: M4A file metadata
- **Vorbis**: OGG file metadata
- **FLAC**: FLAC file metadata

## Best Practices

### 1. Search Optimization
- Use specific song names and artist names
- Avoid using overly vague keywords
- Can include album name for increased accuracy

### 2. Cache Management
- Regularly clean unnecessary cache files
- Monitor cache directory size
- Use force refresh to get latest music list

### 3. Network Optimization
- Ensure stable network connection
- Prioritize local music when network is poor
- Set appropriate timeout duration

### 4. User Experience
- Provide clear playback status feedback
- Support fast responsive control operations
- Gracefully handle playback errors

## Troubleshooting

### Common Issues
1. **Cannot Search Songs**: Check network connection and API availability
2. **Playback Failure**: Check audio devices and file formats
3. **Lyrics Not Displaying**: Check lyrics service and song ID
4. **Local Music Not Showing**: Check file permissions and format support

### Debugging Methods
1. Check log output for detailed error information
2. Test network connection and API response
3. Verify audio file integrity
4. Check cache directory permissions

### Performance Optimization
1. Reasonably set cache strategy
2. Optimize network request frequency
3. Use asynchronous operations to avoid blocking
4. Regularly clean temporary files

With Music Tools, you can enjoy rich music experiences including online search, local playback, lyrics display, and other functions.
