# Lab 23: Building Automation Pipelines

This repository contains the Lab 23 automation pipeline implementation.

## Python files

- `scripts/workflow_functions.py` — CSV processing, report generation, and cleanup
- `automation_pipeline.py` — scheduled automation pipeline with logging and retry logic
- `test_workflow.py` — workflow function tests
- `check_pipeline_status.py` — pipeline and data status checker
- `pipeline_control.py` — start, stop, and status controls
- `monitor_performance.py` — CPU, memory, disk, log, and data monitoring

All Python `#` comments have been removed as requested. Python docstrings are retained because they are string literals, not comments.

## Setup

```bash
pip3 install -r requirements.txt
```

Create the project directories before running:

```bash
mkdir -p logs data scripts
```

The pipeline processes CSV files from the `data` directory and writes logs to `logs/pipeline.log`.
