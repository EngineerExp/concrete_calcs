# Parameters: notebook path (relative to repo root or data), optional CollapseByDefault
Param(
  [string]$notebook = "..\shear_moment_diagram.ipynb",
  [switch]$CollapseByDefault
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
# Ensure all outputs go into the data folder (script directory)
$outdir = $scriptDir
# If notebook is a relative path, resolve against script dir
if (-not (Test-Path $notebook)){
  $candidate = Join-Path $scriptDir $notebook
  if (Test-Path $candidate) { $notebook = $candidate }
}
$nbPath = Resolve-Path $notebook
$base = [System.IO.Path]::GetFileNameWithoutExtension($nbPath)
$outHtml = Join-Path $outdir "$base.html"
$outCollapsible = Join-Path $outdir "${base}_collapsible.html"

Write-Host "Exporting notebook to HTML: $nbPath -> $outHtml"
python -m nbconvert --to html --output "$base" --output-dir $outdir $nbPath
if ($LASTEXITCODE -ne 0) { Write-Error "nbconvert failed with exit code $LASTEXITCODE"; exit $LASTEXITCODE }

Write-Host "Post-processing to add collapsible headings -> $outCollapsible"
  # script lives in the repo root (one level up from data)
  $script = Join-Path (Split-Path $scriptDir -Parent) "add_collapsible_headings.py"
  $collapseArg = if ($CollapseByDefault) { '--collapse-by-default' } else { '' }
  python $script $outHtml $outCollapsible $collapseArg
if ($LASTEXITCODE -ne 0) { Write-Error "post-processor failed with exit code $LASTEXITCODE"; exit $LASTEXITCODE }

Write-Host "Done. Output: $outCollapsible"