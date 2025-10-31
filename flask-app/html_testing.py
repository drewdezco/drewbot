import pandas as pd
import random

# Generate a random number of rows between 100 and 150
num_rows = random.randint(100, 150)

# Create a DataFrame with 8 columns of business data
data = {
    'Business Name': ['Business ' + str(i) for i in range(num_rows)],
    'Revenue': [random.randint(10000, 1000000) for _ in range(num_rows)],
    'Employees': [random.randint(1, 500) for _ in range(num_rows)],
    'Location': ['Location ' + str(random.randint(1, 50)) for _ in range(num_rows)],
    'Established Year': [random.randint(1980, 2022) for _ in range(num_rows)],
    'Industry': [random.choice(['Retail', 'Technology', 'Finance', 'Healthcare', 'Hospitality']) for _ in range(num_rows)],
    'Rating': [random.uniform(1.0, 5.0) for _ in range(num_rows)],
    'Contact Number': ['(555) ' + str(random.randint(100, 999)) + '-' + str(random.randint(1000, 9999)) for _ in range(num_rows)]
}

business_df = pd.DataFrame(data)

print(business_df)