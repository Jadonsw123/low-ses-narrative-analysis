# Bourdieu's Capital Theory Analysis of Low-SES Student Narratives

## Overview

This project analyzes student narratives from the Low-SES dataset using **Bourdieu's Capital Theory**, **Critical Pedagogy**, and **Ecological Systems Theory** as theoretical frameworks. Student narratives are processed through GPT-4 to identify and categorize:

1. **Economic Capital**: Financial resources, employment, material conditions
2. **Social Capital**: Networks, relationships, institutional connections  
3. **Cultural Capital**: Education, knowledge, cultural practices, credentials
4. **Symbolic Capital**: Status, prestige, recognition, legitimacy

Additionally, the analysis examines:
- **Critical Pedagogy**: Student agency and consciousness of structural barriers
- **Ecological Systems**: Microsystem, mesosystem, exosystem, macrosystem, and chronosystem levels

## Workflow

1. **Data Collection**: Low-SES student narratives from Nahed's dataset
2. **GPT-4 Analysis**: `gpt4_three_theory_analyzer.py` codes narratives using all three theoretical frameworks
3. **Visualization**: `visualize_results.py` generates publication-quality diagrams and summary statistics

## Installation

### Requirements
- Python 3.8+
- OpenAI API key (for GPT-4 access)
- Dependencies listed in `requirements.txt`

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"  # Linux/Mac
set OPENAI_API_KEY=your-api-key-here        # Windows
```

## Usage

### Step 1: Prepare Data
Ensure `Low_SES_Collected_dataset.csv` is available (from Nahed's repository)

### Step 2: Run GPT-4 Analysis
```bash
python gpt4_three_theory_analyzer.py
```
This generates checkpoint files in `results/` as it processes narratives in batches of 50.

### Step 3: Generate Visualizations
```bash
python visualize_results.py
```
This creates all publication-quality charts from the analysis results.

## Output Files

The project generates the following outputs in the `results/` directory:

### Analysis Results
- **gpt4_checkpoint_*.json**: Intermediate results (saved every 50 narratives for safety)
- **gpt4_raw_results.json**: Complete analysis of all narratives

### Visualizations (PNG)
- **01_agency_consciousness_scatter.png**: Awareness-action gap analysis
- **02_bourdieu_capital_heatmap.png**: Capital type distributions
- **03_ecological_systems_bar.png**: Dominant system levels
- **04_capital_profile_distribution.png**: Asset/deficit/absent patterns
- **05_agency_distribution.png**: Critical pedagogy agency levels
- **06_consciousness_distribution.png**: Barrier consciousness levels

## Theoretical Framework

### Bourdieu's Capital Forms
The analysis identifies whether each capital form is present as an **asset** (strength), **deficit** (barrier), or **absent** in each narrative.

### Critical Pedagogy
- **Student Agency**: Capacity to act on barriers (high/moderate/low)
- **Consciousness of Barriers**: Awareness of structural inequities (high/moderate/low)

### Ecological Systems
Maps narratives to the primary system level affecting the student's experience.

#### Symbolic Capital
**Deficits**: stigma/shame, low expectations, imposter anxiety
**Assets**: recognition/prestige, agency/resilience

### Analysis Process

1. **Data Loading**: Reads narratives and existing annotations (Background, Struggles, Solutions)
2. **Tokenization & Cleaning**: Processes text with NLTK
3. **Indicator Matching**: Counts capital indicators in each narrative
4. **Scoring**: Calculates deficit counts, asset counts, and net capital scores
5. **Sentiment Analysis**: Uses VADER to assess narrative tone
6. **Export & Visualization**: Generates CSV results and PNG visualizations

## Interpreting Results

### CSV Output Columns

- `sentiment_score`: VADER sentiment (-1 to +1)
- `text_length`: Word count of narrative
- `{capital}_deficit_count`: Number of deficit indicators found
- `{capital}_asset_count`: Number of asset indicators found  
- `{capital}_net_capital`: Assets minus deficits (positive = more assets)
- `{capital}_dominant_deficit`: Most common deficit type for that capital

### Key Metrics

- **Mean Deficits/Assets**: Average number of indicators per narrative
- **Total Deficit/Asset Narratives**: Count and percentage of narratives mentioning each
- **Net Capital**: Positive scores indicate stronger assets than deficits

## Theoretical Foundation

This analysis is grounded in:
- **Bourdieu, P.** (1986). "The Forms of Capital." In *Handbook of Theory and Research for the Sociology of Education*
- Research by Khan et al. on socioeconomic disparities in engineering education
- Abdelgaber et al.'s work on hybrid AI-human annotation of low-SES narratives

## Paper Integration

### For Overleaf/LaTeX
Results are formatted for easy import:
1. Copy tables from PNG visualizations or CSV files
2. Use `booktabs` package for CSV → LaTeX tables
3. Include PNG visualizations directly with `\includegraphics{}`

### Recommended Sections
- **Results**: Include capital summary table and net capital scores
- **Findings**: Discuss dominant deficits and sentiment correlations
- **Discussion**: Interpret capital gaps through Bourdieu's lens

## Customization

To adjust capital indicators, edit the `capital_indicators` dictionary in the `BourdieuCapitalAnalyzer` class:

```python
self.capital_indicators = {
    'economic': {
        'deficits': {
            'your_category': ['keyword1', 'keyword2', ...],
            ...
        },
        'assets': { ... }
    },
    ...
}
```

## Limitations

- Keyword-based coding may miss implicit indicators
- Sentiment analysis based on English language primarily
- Results sensitive to keyword definitions
- No validation against human coding (future work)

## Contact

Working with:
- Dr. Labiba Jahan (SMU)
- Collaborators on inflection_point_equity_research.txt and bridging_socioeconomic_gap_education.txt

## License

Part of the CoNLL 2025 research initiative on low-SES student experiences in education.
