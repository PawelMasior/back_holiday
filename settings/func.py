import os
import autogen
import shutil 
import tiktoken

def clean_memory():
    Paths = [
        os.path.join('.cache', '41'),
        os.path.join('.cache', '44'),
        # os.path.join('monitor', 'actions'),
        # os.path.join('monitor', 'prtscn'),
        ]
    for path in Paths:
        try: 
            shutil.rmtree(path)
            os.mkdir(path)
        except Exception as e:
            print(f"Warning: Clean up files: {str(e)[:200]}")
    try: 
        if os.path.isfile(os.path.join('review', 'logs.db')):
            autogen.runtime_logging.stop()
            os.remove(os.path.join('review', 'logs.db'))        
    except Exception as e:
        print(f"Warning: Clean up logs.db: {str(e)[:200]}")
    if 'temporary' in os.listdir(): shutil.rmtree(os.path.join('temporary'))
    if not 'temporary' in os.listdir(): os.mkdir(os.path.join('temporary'))        

def nr_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    encoding_map = {
        "gpt-3.5-turbo": "cl100k_base",
        "gpt-4": "cl100k_base",
        "text-davinci-003": "p50k_base",
    }
    encoding_name = encoding_map.get(model)
    if encoding_name is None:
        raise ValueError(f"Encoding for model '{model}' is not defined.")
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    return len(tokens)


def dir_files():
    directory = os.getcwd()
    file_entries = []
    for root, dirs, files in os.walk(directory):
        if not sum([s in root for s in ['git', '__pycache__','.cache']]):
            print(root)
            for file in files:
                # Create a relative path to the file
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                relative_path = relative_path.replace(directory,'')
                # Create a Markdown entry for the file
                file_entry = f"- [{relative_path}]({relative_path})"
                file_entry = f"- {relative_path}"
                file_entries.append(file_entry)
    file_entries = [f for f in file_entries if """review\\reports""" not in f]
    file_entries = [f for f in file_entries if 'monitor' not in f]
    markdown_files = '\n'.join(file_entries)
    print(markdown_files)
