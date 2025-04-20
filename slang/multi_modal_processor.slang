system: MultiModalProcessor
version: 1.0
description: System for processing multiple types of inputs and outputs

context:
  user_ci_score: 0.85
  capabilities:
    - text_processing
    - image_analysis
    - audio_processing
    - data_visualization
  preferences:
    processing_mode: parallel
    output_format: mixed
  metadata:
    max_input_size: "10MB"
    supported_formats:
      text: ["txt", "md", "json"]
      image: ["jpg", "png", "svg"]
      audio: ["mp3", "wav"]
      data: ["csv", "json", "xml"]

function: process_text
agent: TextProcessor
intent: Process and analyze text content
context:
  input_types:
    - plain_text
    - markdown
    - structured_data
  processing_steps:
    - tokenization
    - sentiment_analysis
    - entity_extraction
  output_formats:
    - analysis_report
    - visualization
    - summary
input: text_content
output: text_analysis

function: analyze_image
agent: ImageProcessor
intent: Analyze and process images
context:
  analysis_types:
    - object_detection
    - scene_recognition
    - text_extraction
  processing_options:
    resolution: high
    color_space: RGB
    format: png
  metadata:
    max_dimensions: "1920x1080"
    supported_colorspaces: ["RGB", "CMYK", "Grayscale"]
input: image_data
output: image_analysis

function: process_audio
agent: AudioProcessor
intent: Process and analyze audio content
context:
  processing_types:
    - speech_recognition
    - sound_classification
    - audio_enhancement
  audio_settings:
    sample_rate: 44100
    channels: stereo
    format: wav
  metadata:
    max_duration: "5m"
    supported_bitrates: ["128kbps", "256kbps", "320kbps"]
input: audio_data
output: audio_analysis

function: generate_report
agent: ReportGenerator
intent: Generate comprehensive analysis report
context:
  report_types:
    - summary
    - detailed
    - visualization
  output_formats:
    - markdown
    - html
    - pdf
  include:
    - key_findings
    - visualizations
    - recommendations
input:
  - text_analysis
  - image_analysis
  - audio_analysis
output: final_report 