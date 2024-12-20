directory = "data/accounts_key/"
import os
files = [f[:-4] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
print(files)