import PyPDF2
import openai

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text


def generate_resume(user_description, job_interactions=None):
    # Construct the prompt
    prompt = f"請根據以下描述補全簡歷：{user_description}"
    if job_interactions:
        prompt += f" 和互動記錄：{job_interactions}"
    
    try:
        # Make the API request
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",  # Ensure this model name is correct
            prompt=prompt,
            max_tokens=1000
        )
        
        # Adjust based on the actual response structure
        return response.choices[0].text
    except Exception as e:
        # Handle potential errors
        print(f"An error occurred: {e}")
        return None