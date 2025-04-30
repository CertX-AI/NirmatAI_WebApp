# NirmatAI Submission System Web Application

Welcome to the **NirmatAI Submission System**, a web application designed to streamline the submission and processing of documents and requirements for review. This application provides a user-friendly interface for uploading files, reviewing submissions, and initiating processing workflows.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage Guide](#usage-guide)
  - [User Authentication](#user-authentication)
  - [Document Upload (Tab 1)](#document-upload-tab-1)
  - [Requirement Upload (Tab 2)](#requirement-upload-tab-2)
  - [Review & Process Submissions (Tab 3)](#review--process-submissions-tab-3)
- [Directory Structure](#directory-structure)
- [Session Management](#session-management)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

---

## Project Overview

The **NirmatAI Submission System** is built using Streamlit, a Python framework for creating interactive web applications. It enables users to:

- Authenticate with a username (minimum 8 characters).
- Upload documents in various formats (PDF, DOCX, TXT).
- Upload and validate requirements in Excel format.
- Review uploaded files and initiate processing.
- Manage data per user with secure storage.

This system is particularly useful for organizations needing a streamlined way to collect and process documents and requirements from multiple users.

---

## Features

- **User Authentication**: Secure login with username validation and tracking user with MLFlow.
- **Multi-format Document Upload**: Supports PDF, DOCX, and TXT files.
- **Excel Requirement Upload**: Validates Excel files against required columns.
- **Session Management**: Utilizes `st.session_state` for stateful interactions.
- **Dynamic UI Updates**: Immediate interface updates upon actions like login/logout.
- **Data Persistence**: Stores files in a structured directory per user.
- **Error Handling**: Provides clear messages for user actions and validations.
- **Custom Styling**: Enhanced UI with custom CSS for a better user experience.

---

## Technology Stack

- **Python 3.12+**
- **Streamlit**
- **Pandas**
- **OS Module**
- **Regular Expressions (`re` Module)**
- **NirmatAI SDK**

---

## Getting Started

### Prerequisites

- Python 3.12 or higher installed.
- `pip` package manager.
- Internet connection for installing dependencies.

### Installation

1. **Clone the Repository**

### Steps to Clone the Repository

1. **Open Terminal or Command Prompt**

  - **Windows**: You can use Git Bash or Command Prompt.
  - **macOS/Linux**: Use Terminal.

2. **Test SSH Connection (Optional but Recommended)**

   Before cloning, verify that you can connect to the Git server via SSH:

   ```bash
   ssh git@192.168.1.60
   ```

   - If this is your first time connecting, you may be prompted to accept the server's host key.
   - If you receive a permission denied error, ensure your SSH keys are correctly configured.

3. **Clone the Repository**

   Navigate to the directory where you want to install the application and run:

   ```bash
   git clone git@192.168.1.60:CertX/NirmatAI_WebApp.git
   ```

   Example:

   ```bash
   cd /path/to/your/projects
   git clone git@192.168.1.60:CertX/NirmatAI_WebApp.git
   ```

4. Navigate to the Project Directory

   ```bash
   cd NirmatAI_WebApp
   ```

2. **Create a Virtual Environment (Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Ensure `requirements.txt` includes:

   ```
   streamlit
   pandas
   ```

4. **Run the Application**

   ```bash
   streamlit run nirmatai_webapp/streamlit_app.py --server.port=8501
   ```

---

## Usage Guide

### User Authentication

Upon launching the app:

- **Login Process**:
  - Enter a username with at least **8 characters**.
  - Click the **"Login"** button.
  - The app will rerun, and you'll see a welcome message in the sidebar.
- **Username Validation**:
  - The app uses a regex check to ensure the username meets the length requirement.
  - If invalid, an error message prompts for a correct username.
- **Logout Process**:
  - Click the **"Logout"** button in the sidebar.
  - The session resets, and you'll return to the login prompt.

**Note**: The system currently uses a placeholder authentication mechanism. For production, integrate a secure authentication system.

---

### Document Upload (Tab 1)

- **Accessing the Tab**:
  - Navigate to **"📂 Document Upload"**.
- **Uploading Documents**:
  - Supported formats: **PDF**, **DOCX**, **TXT**.
  - Click on the uploader or drag and drop files.
  - You can upload multiple files at once.
- **File Handling**:
  - Uploaded files are saved in `uploaded_files/<username>/documents/`.
  - The app displays a list of uploaded files categorized by type.
- **Submission**:
  - Click **"Submit Documents"** to finalize your upload.
  - Success or error messages provide feedback.

---

### Requirement Upload (Tab 2)

- **Accessing the Tab**:
  - Navigate to **"📑 Requirement Upload"**.
- **Uploading Requirements**:
  - The Excel file must contain these columns:
    - **Requirement Title**
    - **Requirement**
    - **Requirement ID**
    - **Potential Means of Compliance**
    - **Label**
  - A mockup example is provided for reference.
- **Validation**:
  - The app checks for the presence of required columns.
  - If validation passes, the requirements are displayed.
- **File Handling**:
  - The file is saved in `uploaded_files/<username>/requirements/`.
- **Submission**:
  - Click **"Submit Requirements"** to finalize your upload.
  - Appropriate messages confirm the status.

---

### Review & Process Submissions (Tab 3)

- **Accessing the Tab**:
  - Navigate to **"📋 Review & Process"**.
- **Reviewing Submissions**:
  - **Left Column**: Lists uploaded documents.
  - **Right Column**: Shows the requirements file and the first 5 columns of data.
- **Processing Requirements**:
  - Click **"Process Requirements"**.
  - The app searches for the `.xlsx` file in your requirements folder.
  - A success message confirms processing has been initiated.
- **Error Handling**:
  - If no files are found, error messages guide you.

---

## Directory Structure

Upon uploads, the app creates a structured directory:

```
NirmatAI_WebApp/
├── .forgejo
    └── workflows/
        └──  deploy.yml
├── uploaded_files/
    ├── userx/
    │   ├── documents/
    │   │   ├── file1.pdf
    │   │   └── file2.docx
    │   └── requirements/
    │       └── requirements.xlsx
    └── usery/
        ├── documents/
        └── requirements/
├── nirmatai_webapp
    ├── tests/
    │   └── test_nirmatai_sdk.py
    └── streamlit_app.py
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile.client
├── Dockerfile.dev
├── LICENSE
├── Makefile
├── open_webapp.sh
├── pyproject.toml
├── README.md
└── webapp_config.yml
```

- **`uploaded_files/`**: Root folder for all user uploads.
- **`<username>/`**: Folder named after the logged-in user.
- **`documents/`**: Stores uploaded documents.
- **`requirements/`**: Stores the uploaded requirements Excel file.

---

## Session Management

The app uses `st.session_state` to:

- Maintain login status (`logged_in`, `username`).
- Store uploaded files (`uploaded_docs`, `requirements_df`).
- Keep track of file names (`requirements_file_name`).

**Key Points**:

- **State Persistence**: Data persists across tabs during the session.
- **State Reset**: Logging out resets the session state.
- **UI Updates**: The app reruns upon login/logout to reflect changes.

---

## Customization

You can customize the application to suit your needs:

- **UI Styling**: Modify the `custom_css` string to change the look and feel.
- **Authentication**: Integrate with an actual authentication system.
- **File Processing Logic**: Replace placeholder processing code with actual functionality.
- **Validation Rules**: Adjust regex patterns or file validation logic as needed.

---

## Troubleshooting

- **Login Issues**:
  - Ensure the username is at least 8 characters.
  - Check for any whitespace or special characters that might affect the regex.
- **File Upload Errors**:
  - Verify file formats are supported.
  - Ensure the Excel file contains all required columns.
- **Session Problems**:
  - If the app doesn't update after actions, try refreshing the page.
  - Check the console for any error messages.

---

## Contributing

We welcome contributions! To contribute:

1. **Fork the Repository**:

   ```bash
   git clone git@192.168.1.60:CertX/NirmatAI_WebApp.git
   ```

2. **Create a Branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes and Commit**:

   ```bash
   git commit -am "Add new feature"
   ```

4. **Push to GitHub**:

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Submit a Pull Request**.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Contact Information

For questions or support:

- **Project Maintainer**: Ilker Gül
- **Email**: ilker.gul@certx.com
- **Website**: [CERTX](https://www.certx.com)

---

Thank you for using the NirmatAI Submission System! We hope this tool enhances your document and requirement submission processes.
