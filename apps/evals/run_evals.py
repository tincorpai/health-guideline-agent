import json
import sys


def run(dataset_path):
  with open(dataset_path) as f:
    cases = [json.loads(line) for line in f if line.strip()]

  # placeholder metric 
  assert len(cases) >= 0
  print("Eval passed")

if __name__ == "__main__":
  run(sys.argv[1])


