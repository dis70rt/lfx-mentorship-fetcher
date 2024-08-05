# LFX Mentorship Project Data Fetcher

This project is a Python-based client to interact with the Linux Foundation Mentorship API. It fetches project data, converts it into JSON and CSV formats, and allows saving the data to files.

## Features

- Fetches project data from the Linux Foundation Mentorship API.
- Converts the data to JSON format.
- Converts the data to CSV format.
- Saves the fetched data to JSON and CSV files.
- Automatically creates the `data` directory if it does not exist.

## Requirements

- Python 3.x
- `requests` library
- `csv` library
- `io` library
- `json` library
- `os` library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/iit-saikat/lfx-mentorship-fetcher.git
    ```

2. Navigate to the project directory:

    ```bash
    cd lfx-mentorship-fetcher
    ```

3. Install the required libraries:

    ```bash
    pip install requests
    ```

## Usage

1. Initialize the `LFXClient`:

    ```python
    from LFX import LFXClient

    client = LFXClient()
    ```

2. Get the data in JSON format:

    ```python
    json_data = client.json()
    print(json_data)
    ```

3. Get the data in CSV format:

    ```python
    csv_data = client.csv()
    print(csv_data)
    ```

4. Save the data to a CSV file:

    ```python
    client.save_csv("LFX_mentorship.csv")
    ```

5. Save the data to a JSON file:

    ```python
    client.save_json("LFX_mentorship.json")
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.
