import requests
import csv
import io
import json
import os

class LFXClient:
    """
    LFXClient is a class to interact with the Linux Foundation Mentorship API to fetch project data,
    and convert it into JSON and CSV formats. It also allows saving the data to files.
    """
    
    def __init__(self) -> None:
        """
        Initializes the LFXClient object, fetches the data from the API, and stores it.
        """
        url = "https://api.mentorship.lfx.linuxfoundation.org/projects/cache/paginate"

        querystring = {
            "from": "0",
            "size": "100",
            "sortby": "updatedStamp",
            "order": "desc",
            "status": "open",
            "accepting": "true"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Origin": "https://mentorship.lfx.linuxfoundation.org",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "TE": "trailers"
        }

        response = requests.get(url, params=querystring, headers=headers)
        self.data = response.json()

        if 'message' in self.data:
            print("Failed to Fetch Data")
            exit(1)

    def json(self):
        """
        Converts the fetched data into a list of dictionaries in JSON format.
        
        Returns:
            List[Dict]: A list of dictionaries containing project details.
        """
        infos = []
        for item in self.data['hits']['hits']:
            data = item['_source']

            mentors = [{
                "name": mentor.get('name'),
                "email": mentor.get('email'),
                "introduction": mentor.get('introduction')
            } for mentor in data['apprenticeNeeds']['mentors']]

            programTerms = {
                "activeUsers": data['programTerms'][0].get('activeUsers'),
                "name": data['programTerms'][0].get('name'),
                "Active": data['programTerms'][0].get('Active')
            }

            info = {
                "name": data['name'],
                "repository": data['repoLink'],
                "industry": data['industry'],
                "description": data['description'],
                "skills": data['apprenticeNeeds']['skills'],
                "mentors": mentors,
                "programTerms": programTerms
            }
            
            infos.append(info)

        return infos
    
    def csv(self):
        """
        Converts the fetched data into CSV format and returns it as a string.
        
        Returns:
            str: A CSV string containing project details.
        """
        infos = self.json()

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["name", "repository", "industry", "description", "skills", "mentors", "programTerms"])

        for info in infos:
            mentors_str = "; ".join([f"{mentor['name']} ({mentor['email']}): {mentor['introduction']}" for mentor in info['mentors']])
            programTerms_str = f"Active Users: {info['programTerms']['activeUsers']}, Name: {info['programTerms']['name']}, Active: {info['programTerms']['Active']}"
            
            writer.writerow([
                info['name'],
                info['repository'],
                info['industry'],
                info['description'],
                ", ".join(info['skills']),
                mentors_str,
                programTerms_str
            ])

        csv_data = output.getvalue()
        output.close()

        return csv_data
    
    def save_csv(self, filename="LFX_mentorship.csv"):
        """
        Saves the fetched data in CSV format to a file.
        
        Args:
            filename (str): The name of the file to save the CSV data. Defaults to "LFX_mentorship.csv".
        """
        os.makedirs("data", exist_ok=True)
        with open(f"data/{filename}", "w", encoding="utf-8") as file:
            file.write(self.csv())

    def save_json(self, filename="LFX_mentorship.json"):
        """
        Saves the fetched data in JSON format to a file.
        
        Args:
            filename (str): The name of the file to save the JSON data. Defaults to "LFX_mentorship.json".
        """
        os.makedirs("data", exist_ok=True)
        with open(f"data/{filename}", "w", encoding="utf-8") as file:
            json.dump(self.json(), file, indent=4)
