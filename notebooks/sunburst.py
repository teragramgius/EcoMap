import pandas as pd
import plotly.express as px

###############################################
# 1. READ THE CLEAN CSV
###############################################
df = pd.read_csv("data/processed/researchers.csv")  
# Make sure 'researchers_corrected.csv' has 6 columns each row:
# [Name, Academic Position, Department, Network Node Width, Research Interests, Project]

###############################################
# 2. SPLIT 'Research Interests' INTO A LIST
###############################################
# Some rows have multiple interests separated by commas, so we create a list of them.
df['Interests_List'] = df['Research Interests'].fillna('').apply(
    lambda x: [item.strip() for item in x.split(',') if item.strip()]
)

###############################################
# 3. DEFINE A PARTIAL MAPPING FOR (MACROAREA, MICROTOPIC)
#    We want to capture "Ageing / Gerontology" for the keyword "ageing"
###############################################
interest_mapping = [
    # (keyword, macroarea, microtopic)
    ("ageing", "Ageing / Gerontology", "Ageing"),
    ("alzheimer", "Ageing / Gerontology", "Alzheimer"),
    ("longevity", "Ageing / Gerontology", "Longevity"),
    ("stem cells", "Biomed / Cell Biology", "Stem Cells"),
    ("cornea transplant", "Biomed / Surgery", "Cornea Transplant"),
    ("leukemia", "Molecular / Genetics", "Leukemia"),
    ("gene", "Molecular / Genetics", "Gene"),
    ("data science for", "Data Science", "Data Science for"),
    ("data science", "Data Science", "Data Science"),
    ("deep learning", "Data Science / AI", "Deep Learning"),
    ("machine learning", "Data Science / AI", "Machine Learning"),
    ("digital health", "Data Science / eHealth", "Digital Health"),
    ("ai for medical devices", "Data Science / AI", "AI for medical devices"),
    ("urban policy", "Urban / Architecture", "Urban policy"),
    ("urban planning", "Urban / Architecture", "Urban planning"),
    ("migration", "Social / Migration", "Migration"),
    ("emigration", "Social / Migration", "Emigration"),
    ("immunology", "Biomed / Immunology", "Immunology"),
    ("biomechanics", "Medical Engineering", "Biomechanics"),
    ("biomedical database", "Medical Engineering", "Biomedical Database"),
    ("3d print", "Engineering / 3D Tech", "3D Print"),
    ("3d printing", "Engineering / 3D Tech", "3D Printing"),
    ("virtual reality", "Engineering / 3D Tech", "Virtual Reality"),
    ("augmented reality", "Engineering / 3D Tech", "Augmented Reality"),
]

def map_interest_to_macro_and_micro(interest):
    """
    Return (macroarea, microtopic) for a single interest string,
    based on partial keyword matching in interest_mapping.
    Defaults to ("Other", interest) if no match is found.
    """
    lower_interest = interest.lower()
    for (keyword, macro, micro) in interest_mapping:
        if keyword in lower_interest:
            return (macro, micro)
    # fallback if no keyword match
    return ("Other", interest.strip())

###############################################
# 4. BUILD A LONG-FORM DATAFRAME FOR SUNBURST
###############################################
rows = []
for _, row in df.iterrows():
    person = row['Name']
    dept   = row['Department']
    
    # Each interest in 'Interests_List'
    for interest in row['Interests_List']:
        macro, micro = map_interest_to_macro_and_micro(interest)
        rows.append({
            "Name": person,
            "Department": dept,
            "Macroarea": macro,
            "Microtopic": micro
        })

df_long = pd.DataFrame(rows)

###############################################
# 5. SUNBURST A: SHOW ALL MACROAREAS, 
#    BUT MAKE "Ageing / Gerontology" RED
###############################################
macroarea_colors = {
    "Ageing / Gerontology": "#FF0000",  # Red
    "Other": "#808080",                # Gray
    # Add more if you want specific colors 
    # for e.g. "Data Science", "Biomed / Surgery", etc.
}

fig_all = px.sunburst(
    df_long,
    path=["Department", "Macroarea", "Name"],  
    # We use 3 levels: Department (outer) -> Macroarea (middle) -> Name (inner)
    color="Macroarea",   
    color_discrete_map=macroarea_colors,  
    # If a macroarea isn't in 'macroarea_colors', Plotly picks a default color.
    title="Sunburst A: Dept → Macroarea → Name (Ageing in RED)"
)
fig_all.update_layout(margin=dict(t=50, l=50, r=50, b=50))
fig_all.show()

###############################################
# 6. SUNBURST B: FILTER ONLY "Ageing / Gerontology"
#    FOR A FOCUSED VIEW
###############################################
df_ageing = df_long[df_long["Macroarea"] == "Ageing / Gerontology"]

fig_ageing = px.sunburst(
    df_ageing,
    path=["Department", "Name"],  # We can keep it simpler: Dept -> Name
    title="Sunburst Diagram: Ageing-Only by Department"
)
fig_ageing.update_layout(margin=dict(t=50, l=50, r=50, b=50))
fig_ageing.show()
