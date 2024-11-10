import os

# Path to the existing CSV file
file_path = 'SEC_Jamboree_1_Womens_5000_Meters_Junior_Varsity_24.csv'
image_folder = 'images'

# Check if the CSV file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

# Function to parse CSV data
def parse_csv(file_path):
    team_scores = []
    individual_results = []
    in_team_scores = False
    in_individual_results = False
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("Place,Team,Score"):
                in_team_scores = True
                in_individual_results = False
                continue
            elif line.startswith("Place,Grade,Name,Athlete Link,Time,Team,Team Link,Profile Pic"):
                in_team_scores = False
                in_individual_results = True
                continue
            elif not line:
                continue

            data = line.split(',')
            if in_team_scores and len(data) >= 3:
                team_scores.append(data[:3])
            elif in_individual_results and len(data) >= 8:
                individual_results.append(data[:8])
    return team_scores, individual_results

# HTML generation function
def generate_html_page(filename, title, subtitle, team_scores, individual_results):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" type="text/css" href="css/reset.css"> 
        <link rel="stylesheet" href="css/style.css">
        <title>Client Project - Results</title>
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
                <section id="team-scores">
                    <h2>Team Scores</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Place</th>
                                <th>Team</th>
                                <th>Score</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    for score in team_scores:
        html_content += f"<tr><td>{score[0]}</td><td>{score[1]}</td><td>{score[2]}</td></tr>"

    html_content += """
                        </tbody>
                    </table>
                </section>
                <section id="individual-results">
                    <h2>Top 3 Results</h2>
    """
    for result in individual_results[:3]:
        athlete_name = result[2]
        image_path = f"{image_folder}/{result[6].split('/')[-2]}.jpg"
        if not os.path.exists(image_path):
            image_path = "images/default.jpg"
        
        html_content += f"""
                    <div class="athlete">
                        <h3>{athlete_name}</h3>
                        <p>Place: {result[0]}</p>
                        <p>Grade: {result[1]}</p>
                        <p>Time: {result[4]}</p>
                        <p>Team: {result[5]}</p>
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

# Parse CSV data
team_scores, individual_results = parse_csv(file_path)

# Generate each page with proper titles and data
generate_html_page("results.html", "Event Summary", "SEC Jamboree #1 Womens 5000 Meters Junior Varsity", team_scores, individual_results)
generate_html_page("mens.html", "Event Summary", "SEC Jamboree #1 Mens Event Summary", team_scores, individual_results)
generate_html_page("womens.html", "Event Summary", "SEC Jamboree #1 Womens 5000 Meters Junior Varsity", team_scores, individual_results)
generate_html_page("grade9.html", "Event Summary", "SEC Jamboree #1 Grade 9 Event Summary", team_scores, individual_results)
generate_html_page("grade10.html", "Event Summary", "SEC Jamboree #1 Grade 10 Event Summary", team_scores, individual_results)
generate_html_page("grade11.html", "Event Summary", "SEC Jamboree #1 Grade 11 Event Summary", team_scores, individual_results)
