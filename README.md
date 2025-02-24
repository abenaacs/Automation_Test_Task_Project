# LinkedIn Automation Project

This project automates the process of scraping LinkedIn profiles, enriching the data using AI, and storing it in Google Sheets.

## **Features**

- Scrape LinkedIn profiles using PhantomBuster.
- Store scraped data in Google Sheets.
- Enrich data using OpenAI (e.g., generate summaries and outreach messages).
- Automate the workflow using n8n.

## **Setup**

### **Prerequisites**

1. Python 3.9 or higher.
2. PhantomBuster API key.
3. Google Sheets API credentials (`credentials.json`).
4. OpenAI API key.

### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/abenaacs/Automation_Test_Task_Project.git
   cd Automation_Test_Task_Project
   ```

video guide: [video guide](https://www.awesomescreenshot.com/video/36088201?key=9693c9cba1f35e35ba3764ebac016f21)

2. Create a `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```
3. Add your API keys and credentials to the `.env` file.
4. Install dependencies:
   ```bash
   make install
   ```

### **Configuration**

1. Ensure all required API keys and credentials are correctly set in the `.env` file.
2. Update the Google Sheet ID if necessary.

### **Running the Project**

- Run the workflow:
  ```bash
  make run
  ```
- Run tests:
  ```bash
  make test
  ```

## **Workflow**

1. Scrape LinkedIn profiles using PhantomBuster.
2. Append scraped data to Google Sheets.
3. Enrich data using OpenAI.
4. Append enriched data to Google Sheets.

## **CI/CD**

The project uses GitHub Actions for continuous integration. Tests are automatically run on every push or pull request.

## **Contributing**

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request.

## **License**

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

```

```
