import pandas as pd
import plotly.graph_objects as go

# Define the CSV data
data = """Name,Departments,Network Node Width,Interests
Elena Catelli,DIMEVET,4_FullProfessor,"Respiratory viral diseases, Immunology"
Giulia Mescolini,DIMEVET,2_Adjunct professor,"Virus bioinformatics, Molecular diagnostics"
Giulia Quaglia,DIMEVET,2_PhD,"Avian pathology, Immunosuppressive viral diseases, Molecular biology"
Caterina Lupini,DIMEVET,3 Associate Professor Delegate,"Avian vaccines, Immunosuppressive diseases of birds, Respiratory diseases of birds, Viral neoplastic diseases of birds, Recombinant vaccines, Molecular epidemiology"
Zelan Li,Chemistry Department,1_JuniorResearcher,"Heritage Science, Imaging Iperspettrale, Chemiometria, Data Processing, Spettroscopia"
Valentina Orioli,Architecture Department,3_AssociateProfessor,"Municipal urban planning, Local government, Detailed plan, Metropolitan city, Tourism, Colonies, Social housing, Urban regeneration, Public space, Urban project, Mobility, Urban agriculture"
Altea Panebianco,Architecture Department,1_JuniorResearcher,Urban politics
Martina Massari,Architecture Department,1_JuniorResearcher,Enabling city
Francesca Sabatini,Architecture Department,1_Junior Researcher,"Migration, Culture economics, Commons, Urbanistics, Urban planning"
Marco Puleri,SPS,3_Associate Professor,Ukraine War
Gastone Castellani,DIMEC,4_FullProfessor,AI for medical solutions
Nico Curti,DIFA,1_ Junior Researcher,"Protein, Deep learning, Classifier, Network, mRNA, DNA, Sociology, Complex, Applied Sciences, C++, Python, Matlab, Pipeline, Optimization, WSI"
Annalisa Astolfi,DIMEC,2_ Senior Researcher,"Leukemia, Gene"
Marco Viceconti,DIN,4_FullProfessor,"Biomechanics, Orthopedic devices, Ageing"
Giorgio Davico,DIN,1_ Junior Researcher,"Ageing, Biomechanics"
Luca Savelli,DIMEC,3_AssociateProfessor,Sterility
Julia Aleksandra Szyszko,DIN,2_Phd,Computer Methods and Programs in Biomedicine
Riccardo Biondi,DIMEC,2_PHD,"ML for medical solutions, Data Science for Medical Solutions"
Piera Versura,DIMEC,3_AssociateProfessor,"Narrative medicine, Ophthalmology"
Chiara Coslovi,DIMEC,"2, Limited Time Professor","Biomaterials for surgical wound healing, Neurodegenerative diseases, Neuroprotection mechanisms"
Lorenzo Dall'Olio,DIFA,1_Junior Researcher,NLP for medical solutions
Emanuela Marcelli,DICAM,3_ Associate Professor,3D Print
Gloria Astolfi,DICAM,1_ Junior Researcher,Ophthalmology
Nicola Valsecchi,DIMEX,1_ Junior Researcher,Ophthalmology"""

# Load the data into a pandas DataFrame
from io import StringIO
df = pd.read_csv(StringIO(data))

# Split the interests column into individual interests
df['Interests'] = df['Interests'].apply(lambda x: [interest.strip() for interest in x.split(',')] if pd.notna(x) else [])

# Create a list of interest-department relationships with people names
interest_department_people = {}
for index, row in df.iterrows():
    department = row['Departments']
    name = row['Name']
    for interest in row['Interests']:
        if interest not in interest_department_people:
            interest_department_people[interest] = {'departments': {}, 'people': []}
        # Add people to the interest
        interest_department_people[interest]['people'].append(name)
        # Add department to the interest
        if department not in interest_department_people[interest]['departments']:
            interest_department_people[interest]['departments'][department] = 0
        interest_department_people[interest]['departments'][department] += 1

# Now build the Sankey diagram with inflows and without people's names
interests = list(interest_department_people.keys())
departments = list(set(department for interest in interest_department_people.values() for department in interest['departments'].keys()))

# Create mappings for interests and departments to indices
interest_map = {interest: i for i, interest in enumerate(interests)}
department_map = {department: i + len(interests) for i, department in enumerate(departments)}

# Create source, target, value, and label for the Sankey diagram
sources = []
targets = []
values = []
labels = []
# Add interest labels first
labels.extend(interests)
# Add department labels next
labels.extend(departments)

# For each interest, add the flow from interest to departments
for interest, data in interest_department_people.items():
    interest_index = interest_map[interest]
    for department, count in data['departments'].items():
        department_index = department_map[department]
        sources.append(interest_index)
        targets.append(department_index)
        values.append(count)

# Create the Sankey diagram without people's names
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
    )
))

# Show the figure without people's names
fig.update_layout(title_text="Department-Interest Network", font_size=10)
fig.show()
