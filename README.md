# aeroroute-data

Versioned data manifests, validation, transformations, and deterministic
fixtures. It does not serve traffic or optimize routes. Large datasets remain
outside Git; source URL, license, checksum, and provenance belong in manifests.

## MVP airport catalogue

`bundles/mvp-airports-2026.06.27` contains 35 curated international airports
derived from the public-domain OurAirports download. Rebuild it from a current
local source file with:

```bash
uv run aeroroute-data build-mvp-airports \
  --source data/ourairports-airports.csv \
  --output bundles/mvp-airports-2026.06.27 \
  --version 2026.06.27-mvp.1
```

The selection is intentionally small and explicit for the MVP. It broadens
route scenarios without claiming to be an operational airport or navigation
database.
