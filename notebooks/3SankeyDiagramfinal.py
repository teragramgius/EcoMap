import pandas as pd
import plotly.graph_objects as go

#####################################
# 1) READ THE CLEAN CSV
#####################################
df = pd.read_csv("data/processed/researchers.csv")  # path to the saved file

#####################################
# 2) SPLIT INTERESTS INTO A LIST
#####################################
df['Interests_List'] = df['Research Interests'].fillna('').apply(
    lambda x: [item.strip() for item in x.split(',') if item.strip()]
)

#####################################
# 3) DEFINE (MACROAREA, MICROTOPIC) MAPPINGS IF YOU WANT
#####################################
interest_mapping = [
    # (keyword to match lower, macroarea, microtopic)
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

def get_macroarea_and_microtopic(interest):
    lower_interest = interest.lower()
    for (keyword, macro, micro) in interest_mapping:
        if keyword in lower_interest:
            return (macro, micro)
    # fallback
    return ("Other", interest.strip())

#####################################
# 4) BUILD THE MULTI-PART SANKEY
#    Person -> Macroarea -> Microtopic -> Department -> Project
#####################################
current_index = 0
node_map = {}
labels = []
colors = []

def get_node_index(label):
    global current_index
    if not label or pd.isna(label):
        return None
    if label not in node_map:
        node_map[label] = current_index
        labels.append(label)
        colors.append("#A0A0A0")
        current_index += 1
    return node_map[label]

sources = []
targets = []
values = []

for _, row in df.iterrows():
    person = row['Name']
    dept = row['Department']
    project = row['Project']
    
    person_idx = get_node_index(person)
    dept_idx   = get_node_index(dept)
    proj_idx   = get_node_index(project)
    
    for interest in row['Interests_List']:
        macro, micro = get_macroarea_and_microtopic(interest)
        
        macro_idx = get_node_index(macro)
        micro_idx = get_node_index(micro)
        
        # Person -> Macroarea
        sources.append(person_idx)
        targets.append(macro_idx)
        values.append(1)
        
        # Macroarea -> Microtopic
        sources.append(macro_idx)
        targets.append(micro_idx)
        values.append(1)
        
        # Microtopic -> Department
        if dept_idx is not None:
            sources.append(micro_idx)
            targets.append(dept_idx)
            values.append(1)
        
        # Department -> Project (optional)
        if proj_idx is not None:
            sources.append(dept_idx)
            targets.append(proj_idx)
            values.append(1)

fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        label=labels,
        color=colors
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values
    )
))

fig.update_layout(title_text="Multi-Part Sankey: Person → Macroarea → Microtopic → Department → Project",
                  font_size=10)
fig.show()
