system: DataAnalysisSystem
version: 1.0
description: System for data analysis and processing

context:
  user_ci_score: 0.85
  capabilities:
    - data_processing
    - statistical_analysis
    - visualization
    - pattern_recognition
  preferences:
    processing_mode: batch
    visualization_type: interactive
  metadata:
    supported_data_types:
      - numerical
      - categorical
      - time_series
    max_dataset_size: "1GB"

function: preprocess_data
agent: DataPreprocessor
intent: Clean and prepare data for analysis
context:
  preprocessing_steps:
    - handle_missing_values
    - remove_duplicates
    - normalize_data
    - encode_categorical
  data_quality:
    - completeness_check
    - consistency_check
    - accuracy_check
input: raw_data
output: processed_data

function: analyze_trends
agent: TrendAnalyzer
intent: Identify and analyze data trends
context:
  analysis_types:
    - time_series
    - seasonal
    - cyclical
  statistical_methods:
    - moving_average
    - exponential_smoothing
    - regression
  visualization:
    - line_charts
    - scatter_plots
    - heatmaps
input: processed_data
output: trend_analysis

function: generate_insights
agent: InsightGenerator
intent: Generate actionable insights from analysis
context:
  insight_types:
    - descriptive
    - predictive
    - prescriptive
  presentation:
    - summary_statistics
    - key_findings
    - recommendations
  format: markdown
input: trend_analysis
output: data_insights

function: create_report
agent: ReportGenerator
intent: Create comprehensive analysis report
context:
  report_sections:
    - executive_summary
    - methodology
    - findings
    - recommendations
  output_formats:
    - pdf
    - html
    - markdown
  include:
    - visualizations
    - tables
    - appendices
input: data_insights
output: final_report 