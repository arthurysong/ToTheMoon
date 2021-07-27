from pathlib import Path

def get_base_path():
  return Path(__file__).parent

def get_file_path(relative_path): 
  return (get_base_path() / relative_path).resolve()
