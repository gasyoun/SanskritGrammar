#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thin re-run wrapper for H1612 freeze probe — SG-SE-006 (past-tenses).

Delegates to probe_freeze_se_cluster_h1612.py --only=past-tenses.
"""
from pathlib import Path
import runpy
import sys

sys.argv = [sys.argv[0], f"--only=past-tenses"] + sys.argv[1:]
runpy.run_path(str(Path(__file__).with_name("probe_freeze_se_cluster_h1612.py")), run_name="__main__")
