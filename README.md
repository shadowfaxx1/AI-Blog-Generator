
# Video Summarizer

Video Summarizer is a Django-based web application that fetches and summarizes the transcript from any video you love. It's useful for gathering notes on the go. This project leverages AssemblyAI for transcript extraction and Hugging Face's summarization model for summarizing the content. It includes features for user authentication, storing, and viewing blog posts.

## Features
- Fetch and summarize transcripts from YouTube videos.
- User authentication (sign up, login, and logout).
- View, save, and manage summarized blog posts.
- Uses PostgreSQL (via Supabase) for data storage.

## Technologies Used
- Django
- AssemblyAI
- Hugging Face
- PostgreSQL (Supabase)
- Pytube

## Demo Video
[![Watch the video](https://img.youtube.com/vi/Zwcve9oc7NU/maxresdefault.jpg)](https://youtu.be/Zwcve9oc7NU)
## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/video-summarizer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd video-summarizer
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up the PostgreSQL database using Supabase and update the database settings in `settings.py` also see the API keys of the models of assembyAI and huggingFace `blog-generator/Views.py`

7. Apply migrations:
   ```bash
   python manage.py migrate
   ```
8. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage Instructions
1. Access the application at `http://127.0.0.1:8000/`.
2. Sign up or log in to your account.
3. Enter a YouTube video link to fetch and summarize the transcript.
4. View, save, and manage your summarized blog posts.



## Contributing
Contributions are welcome! Please open an issue or submit a pull request with your changes. Ensure your code adheres to the project's coding standards.

## Important Information
- Make sure to replace placeholders with your actual API keys and credentials.
- Ensure your environment is properly configured to use the listed libraries and services.
