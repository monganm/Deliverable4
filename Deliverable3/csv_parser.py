import os

# Paths to the existing CSV files
mens_file_path = 'SEC_Jamboree_1_Mens_5000_Meters_Varsity_24.csv'
womens_file_path = 'SEC_Jamboree_1_Womens_5000_Meters_Junior_Varsity_24.csv'


image_folder = 'images'

# Diagnostic print to check file existence
print("Checking if files exist:")
print("Mens file:", os.path.exists(mens_file_path))
print("Womens file:", os.path.exists(womens_file_path))
print("Current Working Directory:", os.getcwd())

# Function to parse CSV data manually
def parse_csv(file_path):
    individual_results = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        in_individual_results = False
        for line in lines:
            line = line.strip()
            if line.startswith("Place,Grade,Name,Athlete Link,Time,Team,Team Link,Profile Pic"):
                in_individual_results = True
                continue
            elif not line:
                continue

            if in_individual_results:
                data = line.split(',')
                if len(data) >= 8:
                    result = {
                        "Place": data[0],
                        "Grade": int(data[1]),
                        "Name": data[2],
                        "Time": data[4],
                        "Team": data[5],
                        "Profile Pic": data[7]
                    }
                    individual_results.append(result)
    return individual_results

# Function to filter top 3 results by time
def get_top_results(results, top_n=3):
    return sorted(results, key=lambda x: x["Time"])[:top_n]

# Function to filter results by grade and gender
def filter_by_grade(results, grade):
    return [result for result in results if result["Grade"] == grade]

# HTML generation function
def generate_html_page(filename, title, subtitle, individual_results):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" type="text/css" href="css/reset.css"> 
        <link rel="stylesheet" href="css/style.css">
        <title>{title}</title>
    </head>
    <body>
        <header id="main-header">
            <nav id="main-nav">
                <ul>
                    <li><a href="results.html">Results</a></li>
                    <li><a href="mens.html">Mens</a></li>
                    <li><a href="womens.html">Womens</a></li>
                    <li><a href="grade9.html">Grade 9</a></li>
                    <li><a href="grade10.html">Grade 10</a></li>
                    <li><a href="grade11.html">Grade 11</a></li>
                    <li><a href="grade12.html">Grade 12</a></li>
                </ul>
            </nav>
            <h1>{title}</h1>
        </header>
        <div style="text-align: right; padding: 10px; background-color: #f1f1f1; border: 1px solid #000;">
            <button id="darkModeToggle">Toggle Dark Mode</button>
        </div>
        <main id="content">
            <div class="center-container">
                <section id="event-title">
                    <h2>{subtitle}</h2>
                </section>
                <section id="individual-results">
                    <h2>Top Results</h2>
    """
    for result in individual_results:
        athlete_name = result["Name"]
        # Check if 'Profile Pic' is in the result and formatted correctly
        if 'Profile Pic' in result and result['Profile Pic'] and len(result['Profile Pic'].split('/')) > 1:
            image_path = f"{image_folder}/{result['Profile Pic'].split('/')[-2]}.jpg"
        else:
            image_path = "images/default.jpg"
        
        html_content += f"""
                    <div class="athlete">
                        <h3>{athlete_name}</h3>
                        <p>Place: {result['Place']}</p>
                        <p>Grade: {result['Grade']}</p>
                        <p>Time: {result['Time']}</p>
                        <p>Team: {result['Team']}</p>
                        <img src="{image_path}" alt="Profile Picture of {athlete_name}" width="150">
                    </div>
                    <hr>
        """
    
    html_content += """
                </section>
            </div>
        </main>
        <footer id="main-footer">
            <p>&copy; 2024 Client Project - All rights reserved.</p>
        </footer>
        <script>
            const toggleButton = document.getElementById('darkModeToggle');
            toggleButton.addEventListener('click', () => {
                document.body.classList.toggle('dark-mode');
            });
        </script>
    </body>
    </html>
    """

    with open(filename, 'w') as file:
        file.write(html_content)

# Load data
if os.path.exists(womens_file_path):
    women_results = parse_csv(womens_file_path)
else:
    print("Error: Womens file not found.")

if os.path.exists(mens_file_path):
    men_results = parse_csv(mens_file_path)
else:
    print("Error: Mens file not found.")

# Generate general results page - Top 3 Women
if 'women_results' in locals():
    top_women = get_top_results(women_results, 3)
    generate_html_page("results.html", "Top 3 Results", "Top 3 Results - Women", top_women)

# Men's Page - Top 3 Men
if 'men_results' in locals():
    top_men = get_top_results(men_results, 3)
    generate_html_page("mens.html", "Top 3 Men's Results", "SEC Jamboree #1 Men's 5000 Meters Varsity", top_men)

# Women's Page - Top 3 Women
if 'top_women' in locals():
    generate_html_page("womens.html", "Top 3 Women's Results", "SEC Jamboree #1 Women's 5000 Meters Junior Varsity", top_women)

# Grade-specific pages for Women
for grade in [9, 10, 11, 12]:
    if 'women_results' in locals():
        grade_women = filter_by_grade(women_results, grade)
        generate_html_page(f"grade{grade}.html", f"Grade {grade} Women's Results", f"SEC Jamboree #1 Women's Grade {grade}", grade_women)
