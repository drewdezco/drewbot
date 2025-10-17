import pandas as pd
import numpy as np

# Generate random business data for employees
np.random.seed(0)  # For reproducibility
employees = pd.DataFrame({
    'Employee ID': range(1, 101),
    'Name': [f'Employee {i}' for i in range(1, 101)],
    'Department': np.random.choice(['HR', 'Finance', 'IT', 'Sales', 'Marketing'], size=100),
    'Salary': np.random.randint(40000, 120000, size=100),
    'Hire Date': pd.date_range(start='2010-01-01', periods=100, freq='M').date,
    'Performance Score': np.random.uniform(1, 5, size=100).round(2),
    'Status': np.random.choice(['Active', 'Inactive'], size=100)
})

# Save DataFrame to a more attractive HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #e9ecef;
            color: #495057;
            margin: 0;
            padding: 20px;
        }}
        h1 {{
            color: #007bff;
            text-align: center;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        th, td {{
            border: 1px solid #dee2e6;
            padding: 15px;
            text-align: left;
            transition: background-color 0.3s;
        }}
        th {{
            background-color: #007bff;
            color: white;
            text-transform: uppercase;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #d1ecf1;
        }}
        tr:last-child td {{
            border-bottom: 2px solid #007bff;
        }}
    </style>
</head>
<body>
    <h1>Employee Dashboard</h1>
    {table}
</body>
</html>
"""

# Create HTML table from DataFrame
html_table = employees.to_html(index=False)

# Fill in the template with the table
final_html = html_template.format(table=html_table)

# Save the final HTML to a file
with open('employee_dashboard.html', 'w') as f:
    f.write(final_html)