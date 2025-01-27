import pandas as pd
import plotly.graph_objects as go

############################################
# 1) Sample CSV Data
############################################
csv_data = """Name,Departments,Interests,European Project
Alice,DIMEVET,"Urban policies, Digital twins",
Bob,Architecture Department,"Urban regeneration, Digital twins",
Charlie,DIMEC,"AI for medical solutions",
Diana,DIN,"Ageing",
Eric,DIMEVET,"Recombinant vaccines, Immunology",Horizon 2020
"""

############################################
# 2) Dictionary Mapping Interests to (Thematic Area, Microtopic)
############################################
interest_map = {
    "Urban policies": ("Urban Planning", "Urban policies"),
    "Urban regeneration": ("Urban Planning", "Urban regeneration"),
    "Digital twins": ("Data Science", "Digital twins"),
    "AI for medical solutions": ("Data Science", "AI for medical solutions"),
    "Recombinant vaccines": ("Biomed", "Recombinant vaccines"),
    "Immunology": ("Biomed", "Immunology"),
    "Ageing": ("Biomed", "Ageing"),
    # Anything else will default to ("Other", "Other sub-topic")
}

############################################
# 3) Load CSV into a DataFrame
############################################
df = pd.read_csv(pd.io.common.StringIO(csv_data))

# Split 'Interests' column into lists
df['Interests'] = df['Interests'].apply(lambda x: [i.strip() for i in x.split(',')] if pd.notna(x) else [])

############################################
# 4) We'll build a Sankey with the chain:
#    Person -> Thematic Area -> Microtopic -> Department -> (Project optional)
############################################

# We'll keep these as module-level variables
current_index = 0
node_map = {}
labels = []
colors = []

def get_node_index(label):
    """
    Return the node index for a given label.
    If the label is None (e.g., no project), we return None.
    Otherwise, create a new node if not already existing.
    """
    global current_index  # We'll modify current_index in this function
    
    if label is None or pd.isna(label):
        return None
    if label not in node_map:
        node_map[label] = current_index
        labels.append(label)
        # All nodes default to gray (#A0A0A0) here.
        # You can customize color logic if you want different colors for each part.
        colors.append("#A0A0A0")  
        current_index += 1
    return node_map[label]


# We'll store Sankey link data in these lists
sources = []
targets = []
values = []

############################################
# 5) Create the links for each row in df
############################################
for _, row in df.iterrows():
    person = row['Name']
    dept = row['Departments']
    project = row['European Project'] if pd.notna(row['European Project']) else None
    
    # Indices for person & department & project (if present)
    person_idx = get_node_index(person)
    dept_idx = get_node_index(dept)
    project_idx = get_node_index(project)
    
    # For each interest, map to (thematic_area, microtopic)
    for interest in row['Interests']:
        interest = interest.strip()
        if interest in interest_map:
            thematic_area, microtopic = interest_map[interest]
        else:
            thematic_area, microtopic = ("Other", "Other sub-topic")
        
        thematic_idx = get_node_index(thematic_area)
        microtopic_idx = get_node_index(microtopic)
        
        # Build the chain of links:
        # Person -> Thematic Area
        sources.append(person_idx)
        targets.append(thematic_idx)
        values.append(1)
        
        # Thematic Area -> Microtopic
        sources.append(thematic_idx)
        targets.append(microtopic_idx)
        values.append(1)
        
        # Microtopic -> Department
        sources.append(microtopic_idx)
        targets.append(dept_idx)
        values.append(1)
        
        # (Optional) Department -> Project if it exists
        if project_idx is not None:
            sources.append(dept_idx)
            targets.append(project_idx)
            values.append(1)

############################################
# 6) Build and Plot the Sankey Diagram
############################################
fig = go.Figure(go.Sankey(
    arrangement="snap",
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

fig.update_layout(
    title_text="Multi-Part Sankey: Person → Thematic Area → Microtopic → Dept (+ Project)",
    font_size=10
)
fig.show()
