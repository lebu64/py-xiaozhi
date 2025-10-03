# Bazi Fortune Telling Tools (Bazi Tools)

Bazi Fortune Telling Tools is an MCP toolset based on traditional Chinese fortune-telling, providing comprehensive Bazi analysis, marriage compatibility analysis, Chinese almanac query, and other functions.

### Common Usage Scenarios

**Personal Bazi Analysis:**
- "Help me calculate my Bazi, I was born on March 15, 1990 at 3:00 PM"
- "My lunar birthday is February 15, 1985, female, calculate my Bazi"
- "Analyze my destiny characteristics"

**Marriage Compatibility:**
- "Are my partner and I compatible in Bazi? I was born on March 15, 1990, he was born on October 20, 1988"
- "Help us calculate if our marriage is compatible"
- "Analyze our marriage timing"

**Chinese Almanac Query:**
- "Is today a good day?"
- "Chinese almanac information for July 9, 2025"
- "Check what activities are suitable for tomorrow"

**Time Reverse Calculation:**
- "My Bazi is Jiazi year, Bingyin month, Wushen day, Jiayin hour, what are the possible birth times"

### Usage Tips

1. **Provide Accurate Time**: Include year, month, day, and hour information, can be Gregorian or lunar calendar
2. **Specify Gender**: For marriage analysis, please indicate both parties' genders
3. **Natural Description**: Use everyday language to describe your needs, AI will automatically call the appropriate fortune-telling tools
4. **Rational Approach**: Fortune-telling analysis is for reference only, should not be completely relied upon for important decisions

The AI assistant will automatically select appropriate fortune-telling tools based on your needs and provide you with professional Bazi analysis services.

## Feature Overview

### Basic Bazi Analysis
- **Bazi Calculation**: Calculate complete Bazi information based on birth time
- **Five Elements Analysis**: Analyze the strength and preferences of the five elements
- **Ten Gods Analysis**: Analyze the relationships of the ten gods in the destiny
- **Major Life Cycles**: Analyze life fortune trends

### Marriage Analysis
- **Compatibility Analysis**: Analyze whether two people's Bazi are compatible
- **Marriage Timing**: Analyze the best marriage time
- **Spouse Characteristics**: Analyze possible spouse characteristics
- **Marriage Fortune**: Analyze the auspiciousness of married life

### Chinese Almanac Service
- **Daily Auspicious Activities**: Query suitable and unsuitable activities for a specific day
- **Solar Term Information**: Provide 24 solar terms information
- **Lunar Calendar Information**: Provide lunar date and related information

## Tool List

### 1. Basic Bazi Tools

#### get_bazi_detail - Get Bazi Details
Calculate complete Bazi information based on birth time (Gregorian or lunar calendar) and gender.

**Parameters:**
- `solar_datetime` (optional): Gregorian time, format like "1990-03-15 15:30"
- `lunar_datetime` (optional): Lunar time, format like "1990-02-15 15:30"
- `gender` (optional): Gender, 1=male, 0=female, default is 1
- `eight_char_provider_sect` (optional): Bazi school, default is 2

**Usage Scenarios:**
- Personal Bazi analysis
- Fortune-telling consultation
- Fortune prediction foundation

#### get_solar_times - Bazi Reverse Time Calculation
Reverse calculate possible Gregorian birth times based on Bazi information.

**Parameters:**
- `bazi` (required): Bazi information, format like "Jiazi year Bingyin month Wushen day Jiayin hour"

**Usage Scenarios:**
- Time verification
- Multiple possibility analysis
- Bazi verification

#### get_chinese_calendar - Chinese Almanac Query
Query Chinese almanac information for a specified date, including suitable/unsuitable activities, solar terms, etc.

**Parameters:**
- `solar_datetime` (optional): Gregorian time, defaults to current time

**Usage Scenarios:**
- Choosing auspicious dates and times
- Daily suitable/unsuitable activity queries
- Traditional festival information

### 2. Marriage Analysis Tools

#### analyze_marriage_timing - Marriage Timing Analysis
Analyze personal marriage timing and spouse information.

**Parameters:**
- `solar_datetime` (optional): Gregorian time
- `lunar_datetime` (optional): Lunar time
- `gender` (optional): Gender, 1=male, 0=female
- `eight_char_provider_sect` (optional): Bazi school

**Usage Scenarios:**
- Marriage timing prediction
- Spouse characteristic analysis
- Relationship fortune analysis

#### analyze_marriage_compatibility - Marriage Compatibility Analysis
Analyze the marriage compatibility of two people's Bazi.

**Parameters:**
- `male_solar_datetime` (optional): Male Gregorian time
- `male_lunar_datetime` (optional): Male lunar time
- `female_solar_datetime` (optional): Female Gregorian time
- `female_lunar_datetime` (optional): Female lunar time

**Usage Scenarios:**
- Pre-marriage compatibility analysis
- Marriage consultation
- Pairing analysis

## Usage Examples

### Basic Bazi Analysis Examples

```python
# Gregorian time Bazi analysis
result = await mcp_server.call_tool("get_bazi_detail", {
    "solar_datetime": "1990-03-15 15:30",
    "gender": 1
})

# Lunar time Bazi analysis
result = await mcp_server.call_tool("get_bazi_detail", {
    "lunar_datetime": "1990-02-15 15:30",
    "gender": 0
})

# Bazi reverse time calculation
result = await mcp_server.call_tool("get_solar_times", {
    "bazi": "Jiazi year Bingyin month Wushen day Jiayin hour"
})

# Chinese almanac query
result = await mcp_server.call_tool("get_chinese_calendar", {
    "solar_datetime": "2024-01-01"
})
```

### Marriage Analysis Examples

```python
# Personal marriage timing analysis
result = await mcp_server.call_tool("analyze_marriage_timing", {
    "solar_datetime": "1990-03-15 15:30",
    "gender": 1
})

# Two-person marriage compatibility analysis
result = await mcp_server.call_tool("analyze_marriage_compatibility", {
    "male_solar_datetime": "1990-03-15 15:30",
    "female_solar_datetime": "1992-08-20 10:00"
})
```

## Data Structure

### Bazi Information (BaziInfo)
```python
@dataclass
class BaziInfo:
    bazi: str              # Complete Bazi
    year_pillar: dict      # Year pillar information
    month_pillar: dict     # Month pillar information
    day_pillar: dict       # Day pillar information
    hour_pillar: dict      # Hour pillar information
    day_master: str        # Day master
    zodiac: str            # Chinese zodiac
    wuxing_analysis: dict  # Five elements analysis
    shishen_analysis: dict # Ten gods analysis
```

### Marriage Analysis Result (MarriageAnalysis)
```python
@dataclass
class MarriageAnalysis:
    overall_score: float        # Overall score
    overall_level: str          # Marriage compatibility level
    element_analysis: dict      # Element analysis
    zodiac_analysis: dict       # Zodiac analysis
    pillar_analysis: dict       # Day pillar analysis
    branch_analysis: dict       # Earth branch analysis
    complement_analysis: dict   # Complement analysis
    suggestions: list          # Professional suggestions
```

### Chinese Almanac Information (ChineseCalendar)
```python
@dataclass
class ChineseCalendar:
    solar_date: str        # Gregorian date
    lunar_date: str        # Lunar date
    zodiac_year: str       # Zodiac year
    gan_zhi_year: str      # Heavenly stem and earthly branch year
    gan_zhi_month: str     # Heavenly stem and earthly branch month
    gan_zhi_day: str       # Heavenly stem and earthly branch day
    yi_events: list        # Suitable activities
    ji_events: list        # Unsuitable activities
    festival: str          # Festival
    jieqi: str            # Solar term
```

## Professional Terminology Explanation

### Basic Concepts
- **Bazi**: Eight characters composed of heavenly stems and earthly branches from birth year, month, day, and hour
- **Five Elements**: Five basic elements: Metal, Wood, Water, Fire, Earth
- **Ten Gods**: Comparison, Rob Wealth, Food God, Injury Officer, Partial Wealth, Direct Wealth, Seven Killings, Direct Officer, Partial Seal, Direct Seal
- **Major Life Cycles**: Fortune cycles in different life stages
- **Annual Fortune**: Yearly fortune changes

### Marriage Terminology
- **Marriage Compatibility**: Analyze whether two people's Bazi are compatible
- **Six Harmonies**: Best combination relationships between earthly branches
- **Three Harmonies**: Good combination relationships between earthly branches
- **Clash**: Opposition relationships between earthly branches
- **Punishment**: Punishment relationships between earthly branches
- **Harm**: Harm relationships between earthly branches

### Chinese Almanac Terminology
- **Suitable**: Activities suitable to conduct
- **Unsuitable**: Activities not suitable to conduct
- **Solar Terms**: 24 solar terms, reflecting seasonal changes
- **Heavenly Stems and Earthly Branches**: Chinese calendar system

## Precautions

1. **Time Accuracy**: Providing accurate birth time is crucial for analysis results
2. **Rational Approach**: Fortune-telling analysis is for reference only, should not be completely relied upon
3. **Cultural Background**: Based on traditional Chinese culture, requires cultural background knowledge for understanding
4. **Privacy Protection**: Personal birth information is private, please share cautiously

## Best Practices

### 1. Time Formats
- Gregorian time: "YYYY-MM-DD HH:MM" (e.g., "1990-03-15 15:30")
- Lunar time: "YYYY-MM-DD HH:MM" (e.g., "1990-02-15 15:30")
- Ensure time accuracy, especially hour information

### 2. Gender Parameters
- Male: gender=1
- Female: gender=0
- Gender information is important for marriage analysis

### 3. Result Interpretation
- Comprehensively analyze multiple aspects, don't just look at single indicators
- Value professional suggestions and overall scores
- Approach analysis results rationally

### 4. Privacy Protection
- Don't share detailed birth information in public places
- Pay attention to protecting personal privacy and sensitive information

## Troubleshooting

### Common Issues
1. **Time Format Error**: Ensure correct time format
2. **Missing Parameters**: Check if required parameters are provided
3. **Result Interpretation**: Refer to terminology explanation to understand results
4. **Cultural Differences**: Understand traditional cultural background

### Debugging Methods
1. Check time parameter format
2. Verify gender parameter settings
3. Check returned error information
4. Refer to usage examples to adjust parameters

With Bazi Fortune Telling Tools, you can obtain professional fortune-telling analysis services, but please approach analysis results rationally, treating them as life references rather than absolute guidance.
