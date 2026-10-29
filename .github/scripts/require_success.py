"""A skipped/cancelled mandatory check must never turn the aggregate green."""
import json
import os

results = json.loads(os.environ['RESULTS'])
if not results:
    raise SystemExit('No mandatory check results received')
failed = {name: job['result'] for name, job in results.items() if job['result'] != 'success'}
if failed:
    raise SystemExit(f'Mandatory checks did not succeed: {failed}')
print('All mandatory checks passed')
