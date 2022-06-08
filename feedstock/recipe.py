from pangeo_forge_recipes.recipes import XarrayZarrRecipe
from pangeo_forge_recipes.patterns import FilePattern, ConcatDim, MergeDim

# Make FilePattern

# 9 year date range for the variables needed to compute air-sea fluxes
# Notes:
#   - starting from year 78 (instead of 77) since year 77 starts with January 2nd, 
# and all subsequent years start from Jan. 1st
#   - QREFHT and TREFHT are only defined from years 77-86, but QBOT and TBOT are defined
#     from year 46 - 76
years = list(range(78,87))
variables = [
    "LHFLX",
    "SHFLX",
    "FLDS",
    "FSNS",
    "PSL",
    "TAUX",
    "TAUY",
    "TS",
    "U10",
    "QREFHT",
    "TREFHT",
    "UBOT",
    "VBOT"
]

def make_filename(variable, time):
    return ("https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/ASD/"
            "hybrid_v5_rel04_BC5_ne120_t12_pop62/atm-regrid/proc/tseries/daily/FV_768x1152.bilinear."
            f"hybrid_v5_rel04_BC5_ne120_t12_pop62.cam.h1.{variable}.00{time}0101-00{time}1231.nc")
            
            
pattern = FilePattern(
    make_filename,
    ConcatDim(name="time", keys=years),
    MergeDim(name="variable", keys=variables)
)

# Define the recipe

target_chunks = {"time": 73} # Full spatial domain: "lat": 768, "lon": 1152, --> if not specified, will include full extent

recipe = XarrayZarrRecipe(
            file_pattern=pattern,
            target_chunks=target_chunks,
            subset_inputs = {"time": 5}) # set 5 chunks per year, each with time of length 73 (to total 365)