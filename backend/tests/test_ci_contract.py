"""Exercise the actual aggregate program against every mandatory job result."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = yaml.safe_load((ROOT / '.github/workflows/ci.yml').read_text())
JOBS = WORKFLOW['jobs']
MANDATORY = JOBS['required']['needs']


def run_gate(results):
    return subprocess.run([sys.executable, str(ROOT / '.github/scripts/require_success.py')],
                          env={**os.environ, 'RESULTS': json.dumps(results)}, capture_output=True)


def test_gate_covers_every_job_and_runs_after_failure():
    assert set(MANDATORY) == set(JOBS) - {'required'}
    assert JOBS['required']['if'] == 'always()'


@pytest.mark.parametrize('state', ['failure', 'cancelled', 'skipped'])
@pytest.mark.parametrize('job', MANDATORY)
def test_gate_rejects_every_unsuccessful_dependency(job, state):
    results = {name: {'result': 'success'} for name in MANDATORY}
    results[job]['result'] = state
    assert run_gate(results).returncode != 0


def test_gate_passes_only_nonempty_successful_results():
    assert run_gate({name: {'result': 'success'} for name in MANDATORY}).returncode == 0
    assert run_gate({}).returncode != 0


def test_critical_jobs_cannot_be_optional():
    for job in JOBS.values():
        assert not job.get('continue-on-error', False)
        for step in job.get('steps', []):
            assert not step.get('continue-on-error', False)
