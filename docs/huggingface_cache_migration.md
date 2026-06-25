# Hugging Face Cache Migration

The project is configured to use a clear, explicit Hugging Face cache location:

```powershell
C:\Models\HuggingFace
```

The previous cache location was:

```powershell
C:\Users\Slon54\.cache\huggingface
```

The cache contents were copied to the new location. The old cache was not deleted.

## Set The User Environment Variable

Run:

```powershell
.\scripts\set_hf_cache.ps1
```

This runs:

```powershell
setx HF_HOME "C:\Models\HuggingFace"
```

Open a new PowerShell session after running it.

## Run Project Commands With The Cache In The Current Session

Use:

```powershell
.\scripts\run_with_hf_cache.ps1 python run_experiment.py --analysis-only --output-dir results/gpt2
```

The helper sets:

```powershell
$env:HF_HOME = "C:\Models\HuggingFace"
```

for the current command only.

## Verification

A safe verification should use local-only loading so no files are downloaded:

```powershell
$env:HF_HOME = "C:\Models\HuggingFace"
python -c "from transformers import AutoConfig; AutoConfig.from_pretrained('gpt2', local_files_only=True); print('ok')"
```

## Old Cache Cleanup

Do not delete the old cache until you have verified that all needed models load from:

```powershell
C:\Models\HuggingFace
```

After verification, the old cache at `C:\Users\Slon54\.cache\huggingface` can be deleted manually if disk space is needed. This project does not delete it automatically.
