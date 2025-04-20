import pandas as pd

# Load your scraped CSV
df = pd.read_csv("shl_all_assessments_with_time.csv")

# Define your code-to-full-tag mapping
type_mapping = {
    'A': 'Ability & Aptitude',
    'B': 'Biodata & Situational Judgement',
    'C': 'Competencies',
    'D': 'Development & 360',
    'E': 'Assessment Exercises',
    'K': 'Knowledge & Skills',
    'P': 'Personality & Behavior',
    'S': 'Simulations'
}

# Create the new "Tags" column
def expand_tags(test_type_str):
    codes = [code.strip() for code in test_type_str.split(',')]
    tags = [type_mapping.get(code, '') for code in codes if code in type_mapping]
    return ', '.join(tags)

df['Tags'] = df['Test Type'].apply(expand_tags)

# Save it to a new CSV
df.to_csv("shl_all_assessments_with_time_tags.csv", index=False)

print("✅ Done! File saved as 'shl_all_assessments_with_time_tags.csv'")
