"""
GPT-4.1 Three-Theory Analyzer for Student Narratives
====================================================

Codes 387 student narratives against three theoretical frameworks:
1. Critical Pedagogy (Freire)
2. Ecological Systems Theory (Bronfenbrenner)
3. Bourdieu's Theory of Capital & Habitus

Uses OpenAI GPT-4.1 API with validation and error handling.

Usage:
    python gpt4_three_theory_analyzer.py              # Full run (387 narratives)
    python gpt4_three_theory_analyzer.py --test       # Test on 3 narratives
    python gpt4_three_theory_analyzer.py --resume     # Resume from checkpoint
"""

import pandas as pd
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
import sys
from typing import Dict, List, Optional
import logging
from openai import OpenAI, APIError, RateLimitError

# Configure logging with Unicode support for Windows
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gpt4_analysis.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GPT4ThreeTheoryAnalyzer:
    """Analyzes narratives using GPT-4 against three theoretical frameworks."""
    
    def __init__(self, 
                 dataset_path='Low_SES_Collected_dataset.csv',
                 prompt_path='gpt4_coding_prompt.md',
                 api_key: Optional[str] = None,
                 output_dir='./results'):
        """
        Initialize the analyzer.
        
        Args:
            dataset_path: Path to the narrative CSV file
            prompt_path: Path to the GPT-4 prompt template
            api_key: OpenAI API key (will use environment variable if not provided)
            output_dir: Directory to save results
        """
        self.dataset_path = dataset_path
        self.prompt_path = prompt_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Set up OpenAI client (new API v1.0.0+)
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = OpenAI()  # Uses OPENAI_API_KEY environment variable
        
        # Load data
        self.narratives_df = None
        self.results = []
        self.errors = []
        
        self._load_data()
        self._load_prompt()
    
    def _load_data(self):
        """Load the narrative dataset."""
        try:
            self.narratives_df = pd.read_csv(self.dataset_path)
            logger.info(f"✓ Loaded {len(self.narratives_df)} narratives from {self.dataset_path}")
        except FileNotFoundError:
            logger.error(f"❌ Dataset not found at {self.dataset_path}")
            sys.exit(1)
    
    def _load_prompt(self):
        """Load the GPT-4 prompt template."""
        try:
            with open(self.prompt_path, 'r') as f:
                self.prompt_template = f.read()
            logger.info(f"✓ Loaded prompt template from {self.prompt_path}")
        except FileNotFoundError:
            logger.error(f"❌ Prompt template not found at {self.prompt_path}")
            sys.exit(1)
    
    def analyze_narrative(self, narrative_text: str, idx: int) -> Optional[Dict]:
        """
        Use GPT-4 to analyze a single narrative.
        
        Args:
            narrative_text: The student narrative to analyze
            idx: Index of the narrative (for logging)
            
        Returns:
            Parsed JSON response or None if error occurred
        """
        try:
            # Create the prompt with the narrative
            prompt = self.prompt_template.replace("{NARRATIVE_TEXT}", narrative_text)
            
            # Call GPT-4.1 API (new client API)
            response = self.client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in educational theory and qualitative research coding. Return ONLY valid JSON, no markdown or extra text."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Extract and parse response
            response_text = response.choices[0].message.content.strip()
            
            # Try to extract JSON if it's wrapped in markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)
            result['narrative_idx'] = idx
            result['narrative_text'] = narrative_text
            
            logger.debug(f"Successfully analyzed narrative {idx}")
            return result
            
        except json.JSONDecodeError as e:
            error_msg = f"JSON parsing error for narrative {idx}: {str(e)}"
            logger.error(error_msg)
            self.errors.append({
                'idx': idx,
                'error_type': 'JSON_PARSE_ERROR',
                'message': str(e)
            })
            return None
        
        except RateLimitError:
            logger.warning(f"Rate limit hit at narrative {idx}. Waiting 60 seconds...")
            time.sleep(60)
            return self.analyze_narrative(narrative_text, idx)
        
        except APIError as e:
            error_msg = f"API error for narrative {idx}: {str(e)}"
            logger.error(error_msg)
            self.errors.append({
                'idx': idx,
                'error_type': 'API_ERROR',
                'message': str(e)
            })
            return None
        
        except Exception as e:
            error_msg = f"Unexpected error for narrative {idx}: {str(e)}"
            logger.error(error_msg)
            self.errors.append({
                'idx': idx,
                'error_type': 'UNEXPECTED_ERROR',
                'message': str(e)
            })
            return None
    
    def run_analysis(self, n: Optional[int] = None, start_idx: int = 0, save_interval: int = 50):
        """
        Run analysis on narratives.
        
        Args:
            n: Number of narratives to process (None = all)
            start_idx: Start from this index (for resuming)
            save_interval: Save results every N narratives
        """
        if n is None:
            n = len(self.narratives_df)
        
        n = min(n, len(self.narratives_df) - start_idx)
        
        logger.info(f"\n{'='*80}")
        logger.info(f"Starting analysis: {n} narratives (starting at index {start_idx})")
        logger.info(f"{'='*80}\n")
        
        start_time = time.time()
        
        for i in range(start_idx, start_idx + n):
            try:
                # Get narrative
                narrative = self.narratives_df.iloc[i]['Text']
                
                # Analyze with GPT-4
                print(f"[{i-start_idx+1}/{n}] Processing narrative {i}...", end=" ", flush=True)
                result = self.analyze_narrative(narrative, i)
                
                if result:
                    self.results.append(result)
                    print("OK")
                else:
                    print("ERROR (see log)")
                
                # Save checkpoint every N narratives
                if (i - start_idx + 1) % save_interval == 0:
                    self._save_checkpoint(i)
                
                # Rate limiting: ~2-3 requests per second
                time.sleep(0.4)
                
            except KeyboardInterrupt:
                logger.info("\n[!] Analysis interrupted by user")
                self._save_checkpoint(i)
                break
        
        elapsed_time = time.time() - start_time
        logger.info(f"\n{'='*80}")
        logger.info(f"Analysis complete!")
        logger.info(f"  Processed: {len(self.results)} narratives successfully")
        logger.info(f"  Errors: {len(self.errors)}")
        logger.info(f"  Time elapsed: {elapsed_time:.1f} seconds ({elapsed_time/60:.1f} minutes)")
        logger.info(f"{'='*80}\n")
        
        return self.results
    
    def _save_checkpoint(self, idx: int):
        """Save results checkpoint to file."""
        checkpoint_file = self.output_dir / f'gpt4_checkpoint_{idx}.json'
        with open(checkpoint_file, 'w') as f:
            json.dump({
                'results': self.results,
                'errors': self.errors,
                'last_idx': idx,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        logger.info(f"  [CHECKPOINT] saved ({len(self.results)} results)")
    
    def save_raw_results(self, filename: str = 'gpt4_raw_results.json'):
        """Save raw GPT-4 responses as JSON."""
        output_path = self.output_dir / filename
        with open(output_path, 'w') as f:
            json.dump({
                'results': self.results,
                'errors': self.errors,
                'summary': {
                    'total_processed': len(self.results),
                    'total_errors': len(self.errors),
                    'timestamp': datetime.now().isoformat()
                }
            }, f, indent=2)
        logger.info(f"[OK] Saved raw results to {output_path}")
    
    def parse_to_csv(self, output_filename: str = 'gpt4_three_theory_full.csv'):
        """
        Convert raw GPT-4 results to structured CSV format.
        
        Args:
            output_filename: Name of output CSV file
        """
        parsed_rows = []
        
        for result in self.results:
            try:
                row = {
                    'narrative_idx': result.get('narrative_idx'),
                    'narrative_text': result.get('narrative_text'),
                    
                    # Critical Pedagogy
                    'critical_pedagogy_student_agency': result['critical_pedagogy']['student_agency'],
                    'critical_pedagogy_structural_barriers': result['critical_pedagogy']['structural_barriers_evident'],
                    'critical_pedagogy_consciousness': result['critical_pedagogy']['consciousness_of_barriers'],
                    'critical_pedagogy_summary': result['critical_pedagogy']['summary'],
                    
                    # Ecological Systems
                    'ecological_dominant_level': result['ecological_systems']['dominant_level'],
                    'ecological_secondary_level': result['ecological_systems'].get('secondary_level'),
                    'ecological_summary': result['ecological_systems']['summary'],
                    
                    # Bourdieu's Capital
                    'bourdieu_economic': result['bourdieu_capital']['economic'],
                    'bourdieu_social': result['bourdieu_capital']['social'],
                    'bourdieu_cultural': result['bourdieu_capital']['cultural'],
                    'bourdieu_symbolic': result['bourdieu_capital']['symbolic'],
                    'bourdieu_dominant_need': result['bourdieu_capital']['dominant_capital_need'],
                    'bourdieu_dominant_strength': result['bourdieu_capital'].get('dominant_capital_strength'),
                    'bourdieu_summary': result['bourdieu_capital']['summary'],
                    
                    # Overall
                    'overall_summary': result['overall_summary']
                }
                parsed_rows.append(row)
            
            except (KeyError, TypeError) as e:
                logger.warning(f"Error parsing result for narrative {result.get('narrative_idx')}: {str(e)}")
                continue
        
        # Create DataFrame and save
        df = pd.DataFrame(parsed_rows)
        output_path = self.output_dir / output_filename
        df.to_csv(output_path, index=False)
        logger.info(f"[OK] Parsed results to CSV: {output_path}")
        logger.info(f"  Rows: {len(df)}")
        
        return df
    
    def print_sample_results(self, n: int = 3):
        """Print sample results for inspection."""
        logger.info(f"\n{'='*80}")
        logger.info("SAMPLE RESULTS (first 3 narratives)")
        logger.info(f"{'='*80}\n")
        
        for result in self.results[:n]:
            logger.info(f"\nNarrative {result['narrative_idx']}:")
            logger.info(f"  Critical Pedagogy: Agency = {result['critical_pedagogy']['student_agency']}")
            logger.info(f"  Ecological Systems: Dominant level = {result['ecological_systems']['dominant_level']}")
            logger.info(f"  Bourdieu's Capital: {result['bourdieu_capital']['economic']} (econ), {result['bourdieu_capital']['social']} (social), {result['bourdieu_capital']['cultural']} (cultural), {result['bourdieu_capital']['symbolic']} (symbolic)")
            logger.info(f"  Overall: {result['overall_summary'][:100]}...")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Analyze student narratives using GPT-4 and three theoretical frameworks'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run on first 3 narratives for testing'
    )
    parser.add_argument(
        '--n',
        type=int,
        default=None,
        help='Number of narratives to process (default: all)'
    )
    parser.add_argument(
        '--resume',
        type=int,
        default=0,
        help='Resume from narrative index N'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='OpenAI API key (uses environment variable if not provided)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./results',
        help='Directory to save results'
    )
    
    args = parser.parse_args()
    
    # Determine number of narratives to process
    n = 3 if args.test else args.n
    
    # Initialize analyzer
    try:
        analyzer = GPT4ThreeTheoryAnalyzer(
            api_key=args.api_key,
            output_dir=args.output_dir
        )
    except Exception as e:
        if "API key" in str(e) or "No API key" in str(e):
            print("\n[ERROR] OPENAI_API_KEY not found!")
            print("Set it with: $env:OPENAI_API_KEY='your-api-key-here'")
            print("Or pass it with: python script.py --api-key 'your-key'")
        else:
            print(f"[ERROR] {str(e)}")
        return
    
    # Run analysis
    analyzer.run_analysis(n=n, start_idx=args.resume)
    
    # Save results
    analyzer.save_raw_results()
    
    # Parse and export to CSV
    if analyzer.results:
        analyzer.parse_to_csv()
        analyzer.print_sample_results()
    else:
        logger.error("[ERROR] No results to save. Check errors in log file.")
    
    logger.info("\n[OK] Analysis complete! Check 'results' folder for outputs.")
    logger.info(f"  Raw results: gpt4_raw_results.json")
    logger.info(f"  Parsed CSV: gpt4_three_theory_full.csv")
    logger.info(f"  Log file: gpt4_analysis.log")


if __name__ == "__main__":
    main()
