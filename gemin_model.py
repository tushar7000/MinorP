import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import json

genai.configure(api_key="AIzaSyBTXGvzToeXpzeJR5uY6H-rL7rPypMSFYo")  # Replace with your actual API key

class AITutor:
    def __init__(self, model_version='flash'):
        self.topic = None
        self.model_version = model_version
        self.progress = {'quiz_attempted': 0, 'correct_answers': 0, 'topics_completed': []}
        self.model_map = {
            'flash': 'models/gemini-1.5-flash-latest',
            'pro': 'models/gemini-1.0-pro-latest',
            'nano': 'models/gemini-1.0-pro'
        }
        self.coding_topics = ["python", "java", "c++", "javascript", "html", "css", "sql", "data structures", "algorithms"]

    def ask_gemini(self, prompt):
        """Get response from Gemini AI with rich formatting"""
        try:
            model = genai.GenerativeModel(self.model_map[self.model_version])
            response = model.generate_content(prompt)
            if not hasattr(response, 'text'):
                return "Sorry, I couldn't process that request."
            
            # Format the response to maintain interactive-style output
            formatted_response = response.text.replace('\n', '<br>')
            formatted_response = formatted_response.replace('•', '•')
            formatted_response = formatted_response.replace('✅', '✅')
            formatted_response = formatted_response.replace('❌', '❌')
            return formatted_response
            
        except Exception as e:
            print(f"Error: {e}")
            return "Sorry, I'm having trouble responding right now."

    def set_topic(self, topic):
        """Set topic with interactive-style response"""
        self.topic = topic.lower()
        return f"🔹 Topic set to: {self.topic}"

    def get_notes(self, style="detailed"):
        """Generate notes with interactive formatting"""
        prompt = f"""Provide {style} study notes for: {self.topic}. Format with:
        - Clear headings
        - Bullet points
        - Key takeaways
        - Use emojis where appropriate
        - Include examples if relevant"""
        return self.ask_gemini(prompt)

    def get_questions(self):
        """Generate questions with quiz formatting"""
        prompt = f"""Generate questions about {self.topic} with this format:
        
        📝 Multiple Choice Questions:
        1. Question text?
        A) Option 1
        B) Option 2
        C) Option 3
        D) Option 4

        📝 True/False Questions:
        1. Statement (True/False)
        
        Don't include answers."""
        return self.ask_gemini(prompt)

    def get_quiz(self):
        """Generate single quiz question with progress tracking"""
        prompt = f"""Create one quiz question about {self.topic} in this format:
        
        🎯 Quiz Question:
        [MCQ or True/False question]
        Options (if MCQ):
        A) Option 1
        B) Option 2
        etc.
        
        Don't reveal the answer."""
        question = self.ask_gemini(prompt)
        self.progress['quiz_attempted'] += 1
        return question + "\n\nEnter your answer:"

    def check_answer(self, user_answer, correct_answer="A"):
        """Check answer with interactive feedback"""
        if user_answer.lower() == correct_answer.lower():
            self.progress['correct_answers'] += 1
            return "✅ Correct! Well done!"
        else:
            return f"❌ Incorrect. The correct answer was: {correct_answer}"

    def get_flashcards(self):
        """Generate flashcards with Q&A format"""
        prompt = f"""Create 5 flashcards for {self.topic} in this exact format:
        
        📌 Flashcard 1:
        Q: [Question]
        A: [Answer]
        
        📌 Flashcard 2:
        Q: [Question]
        A: [Answer]
        ..."""
        return self.ask_gemini(prompt)

    def get_progress(self):
        """Show progress with visual indicators"""
        attempted = self.progress['quiz_attempted']
        correct = self.progress['correct_answers']
        progress_bar = "[" + "★"*correct + "☆"*(attempted-correct) + "]"
        return f"""📊 Your Progress:
        {progress_bar}
        Correct: {correct}/{attempted}
        Topics: {', '.join(self.progress['topics_completed'])}"""

    def get_best_youtube_videos(self):
        """Get YouTube videos with rich formatting"""
        search_query = self.topic.replace(" ", "+")
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&key=AIzaSyAWrlhCODC6npVZBJLXsYCT6c5KvP3LeKY&maxResults=3"
        
        try:
            response = requests.get(url)
            data = response.json()
            if "items" not in data:
                return "No YouTube videos found."

            videos = []
            for i, item in enumerate(data["items"], 1):
                videos.append(f"""📺 {i}. {item['snippet']['title']}
                https://www.youtube.com/watch?v={item['id']['videoId']}""")
            return "Recommended Videos:\n" + "\n\n".join(videos)
            
        except Exception as e:
            print(f"YouTube API Error: {e}")
            return "Couldn't fetch YouTube videos right now."

    def get_best_resources(self):
        """Get web resources with rich formatting"""
        if not hasattr(self, 'bing_api_key') or self.bing_api_key == "YOUR_BING_API_KEY":
            return "Bing search is not configured."
            
        search_query = self.topic.replace(" ", "+")
        url = f"https://api.bing.microsoft.com/v7.0/search?q=best+resources+for+{search_query}"
        headers = {"Ocp-Apim-Subscription-Key": self.bing_api_key}

        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            if "webPages" not in data:
                return "No web resources found."

            resources = []
            for i, item in enumerate(data["webPages"]["value"][:3], 1):
                resources.append(f"""🔗 {i}. {item['name']}
                {item['url']}""")
            return "Recommended Resources:\n" + "\n\n".join(resources)
            
        except Exception as e:
            print(f"Bing API Error: {e}")
            return "Couldn't fetch web resources right now."

    def get_code_challenges(self):
        """Generate coding challenges with interactive formatting"""
        if not any(topic in self.topic for topic in self.coding_topics):
            return "❌ This topic is not related to coding."

        prompt = f"""Create 3 coding problems for {self.topic} in this format:
        
        💻 Problem 1:
        [Description]
        Sample Input: [example]
        Sample Output: [example]
        
        💻 Problem 2:
        ..."""
        return self.ask_gemini(prompt)