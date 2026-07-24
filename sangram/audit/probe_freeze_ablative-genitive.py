#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thin re-run wrapper for H1612 freeze probe — SG-SE-004 (ablative-genitive).

Delegates to probe_freeze_se_cluster_h1612.py --only=ablative-genitive.
"""
from pathlib import Path
import runpy
import sys

sys.argv = [sys.argv[0], f"--only=ablative-genitive"] + sys.argv[1:]
runpy.run_path(str(Path(__file__).with_name("probe_freeze_se_cluster_h1612.py")), run_name="__main__")
