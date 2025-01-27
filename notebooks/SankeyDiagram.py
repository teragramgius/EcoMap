import pandas as pd
import plotly.graph_objects as go

# Define the CSV data with grades
data = """Name,Grade,Departments,Network Node Width,Interests, Project
Elena Catelli,Full Professor,DIMEVET,4,"Respiratory viral diseases, Immunology",Project A
Giulia Mescolini,Adjunct Professor,DIMEVET,2,"Virus bioinformatics, Molecular diagnostics",
Caterina Lupini,Associate Professor,DIMEVET,3,"Data science for medical solutions, Recombinant vaccines",Project B
Zelan Li,Junior Researcher,Chemistry Department,1,"Heritage Science, Data Processing",Project C
Valentina Orioli,Associate Professor,Architecture Department,3,"Urban regeneration, Public space",
Marco Puleri,Associate Professor,SPS,3,"Ukraine War",
Annalisa Astolfi,Senior Researcher,DIMEC,2,"Leukemia, Gene",Project A
Gastone Castellani,Full Professor,DIMEC,4,"AI for medical solutions",
"""

# Load the data into a pandas DataFrame
from io import StringIO
df = pd.read_csv(StringIO(data))

# Define categories for interests
interest_categories = {
    "Respiratory viral diseases": "Medical Research",
    "Immunology": "Medical Research",
    "Virus bioinformatics": "Bioinformatics",
    "Molecular diagnostics": "Diagnostics",
    "Data science for medical solutions": "Data Science",
    "Recombinant vaccines": "Vaccinology",
    "Heritage Science": "Cultural Heritage",
    "Data Processing": "Data Science",
    "Urban regeneration": "Urban Planning",
    "Public space": "Urban Planning",
    "Ukraine War": "Social Sciences",
    "Leukemia": "Medical Research",
    "Gene": "Genetics",
    "AI for medical solutions": "Artificial Intelligence",
    "Ageing and related diseases": "Ageing",
    "Gene expression in muscles": "Other - Genetics",
    "Body composition and ageing": "Ageing",
    "Insomnia and stress-related responses": "Ageing",
    "Inflammaging and muscle weakness": "Ageing",
    "Anti-ageing strategies": "Ageing",
    "Mitochondria and ageing immunity": "Ageing",
    "Longevity markers and ageing": "Ageing",
    "Nutrition and ageing inflammation": "Ageing",
    "Cognitive decline in Down syndrome": "Ageing",
    "Brain ageing and lipids": "Ageing",
    "Ageing biomarkers in longevity": "Ageing",
    "Muscle lipid metabolism": "Other - Genetics",
    "Muscle recovery from space stress": "Ageing",
    "Tissue remodeling in ageing": "Ageing",
    "Genetic regulation in sex differences": "Other - Genetics",
    "Ageing mechanisms and diseases": "Ageing",
    "Skeletal muscle ageing markers": "Ageing",
    "Muscle inflammation and ageing": "Ageing",
    "Metabolic diseases in ageing": "Ageing",
    "Knee surgery and ageing activity": "Ageing",
    "Muscle ageing and inactivity": "Ageing",
    "Tissue regeneration and ageing": "Ageing",
    "Cellular ageing and inflammaging": "Ageing",
    "Muscle weakness in ageing": "Ageing",
    "Age-related muscle changes": "Ageing",
    "Stem cell protection": "Other - Stem Cell Research",
     "Domestic-wild bird interface and avian influenza": "Other - Veterinary Science",
    "Inflammation mediators in poultry infections": "Other - Veterinary Science",
    "Virus bioinformatics, Molecular diagnostics":  "Other - Veterinary Science",
    "Avian pathology, Immunosuppressive viral diseases, Molecular biology": "Other - Veterinary Science",
}

# Assign categories to interests
df['Interest Types'] = df['Interests'].apply(lambda x: [interest_categories.get(i.strip(), "Other") for i in x.split(',')] if pd.notna(x) else [])

# Define grade weights (based on Network Node Width)
grade_weights = {
    "Junior Researcher": 1,
    "Adjunct Professor": 2,
    "Senior Researcher": 3,
    "Associate Professor": 3,
    "Full Professor": 4
}

# Prepare Sankey diagram data
nodes = []
labels = []
colors = []
sources = []
targets = []
values = []

# Define color mappings for each type
category_colors = {
    "Medical Research": "#FF5733",
    "Bioinformatics": "#33FF57",
    "Diagnostics": "#3357FF",
    "Data Science": "#FFD700",
    "Vaccinology": "#C70039",
    "Cultural Heritage": "#900C3F",
    "Urban Planning": "#1E90FF",
    "Social Sciences": "#FF1493",
    "Genetics": "#8A2BE2",
    "Artificial Intelligence": "#FF8C00",
    "Other": "#808080",
}

# Create mappings for all nodes
node_map = {}
idx = 0

# Add nodes for individuals
for name in df['Name']:
    node_map[name] = idx
    labels.append(name)
    colors.append("#808080")  # Gray for individuals
    idx += 1

# Add nodes for interest types
unique_interest_types = set(interest for sublist in df['Interest Types'] for interest in sublist)
for interest_type in unique_interest_types:
    node_map[interest_type] = idx
    labels.append(interest_type)
    colors.append(category_colors.get(interest_type, "#000000"))  # Use category color or default to black
    idx += 1

# Add nodes for departments
unique_departments = df['Departments'].unique()
for department in unique_departments:
    node_map[department] = idx
    labels.append(department)
    colors.append("#FFD700")  # Yellow for departments
    idx += 1

# Add nodes for Projects
unique_projects = df['Project'].dropna().unique()
for project in unique_projects:
    node_map[project] = idx
    labels.append(project)
    colors.append("#1E90FF")  # Blue for projects
    idx += 1

# Map links (individual -> interest type -> department/project)
for _, row in df.iterrows():
    person = row['Name']
    department = row['Departments']
    project = row['Project']
    grade = row['Grade']
    grade_weight = grade_weights.get(grade, 1)  # Default to 1 if grade not found
    
    # Link individual -> interest types
    for interest_type in row['Interest Types']:
        sources.append(node_map[person])
        targets.append(node_map[interest_type])
        values.append(grade_weight)  # Use grade weight for the flow thickness
    
    # Link interest types -> department
    for interest_type in row['Interest Types']:
        sources.append(node_map[interest_type])
        targets.append(node_map[department])
        values.append(grade_weight)
    
    # Link department -> project (if applicable)
    if pd.notna(project):
        sources.append(node_map[department])
        targets.append(node_map[project])
        values.append(grade_weight)

# Create the Sankey diagram
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=colors
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,  # Adjusted flow thickness based on grade
        color="rgba(0,0,0,0.3)"  # Transparent link color
    )
))

# Show the diagram
fig.update_layout(title_text="Sankey Diagram with Grade-Based Node Widths", font_size=10)
fig.show()
