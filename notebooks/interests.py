import pandas as pd
from collections import Counter

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
all_interests = []
for interests in df['Interests']:
    if pd.notna(interests):  # Ignore NaN values
        all_interests.extend([interest.strip() for interest in interests.split(',')])

# Count the occurrences of each interest
interest_counts = Counter(all_interests)

# Convert to a DataFrame for better visualization
interest_counts_df = pd.DataFrame(interest_counts.items(), columns=['Interest', 'Count'])
interest_counts_df = interest_counts_df.sort_values(by='Count', ascending=False)

# Display the most common interests
print(interest_counts_df)

# Plot the results (optional)
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 8))
plt.barh(interest_counts_df['Interest'], interest_counts_df['Count'], color='skyblue')
plt.xlabel('Count')
plt.ylabel('Interest')
plt.title('Interest Frequency in CSV')
plt.gca().invert_yaxis()  # Reverse the order for better readability
plt.show()


####################### next - interests by department
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

# Create a list of department-interest relationships
department_interest = []
for index, row in df.iterrows():
    department = row['Departments']
    for interest in row['Interests']:
        department_interest.append((department, interest))

# Get a list of unique departments and interests
departments = list(set([x[0] for x in department_interest]))
interests = list(set([x[1] for x in department_interest]))

# Create mappings for departments and interests to indices
department_map = {department: i for i, department in enumerate(departments)}
interest_map = {interest: i + len(departments) for i, interest in enumerate(interests)}

# Create source, target, and value for the Sankey diagram
sources = []
targets = []
values = []
for department, interest in department_interest:
    sources.append(department_map[department])
    targets.append(interest_map[interest])
    values.append(1)  # Each connection counts as 1

# Define the labels for the Sankey diagram
labels = departments + interests

# Create the Sankey diagram
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

# Show the figure
fig.update_layout(title_text="Department-Interest Network", font_size=10)
fig.show()

