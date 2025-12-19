# Groq API Setup Guide

## Why Groq?

Groq offers **free, fast, and generous API limits** for running open-source LLMs like Llama3, making it perfect for development and testing.

### Free Tier Limits:
- **30 requests per minute**
- **14,400 requests per day**
- Fast inference with low latency

Compare this to Gemini's free tier (20 requests/day), and you'll see why Groq is excellent for development!

---

## Getting Your Free Groq API Key

### Step 1: Sign Up
1. Go to [Groq Console](https://console.groq.com/)
2. Click **"Sign Up"** or **"Log In"** if you have an account
3. You can sign up with:
   - Google account
   - GitHub account
   - Email address

### Step 2: Create API Key
1. Once logged in, navigate to [API Keys](https://console.groq.com/keys)
2. Click **"Create API Key"**
3. Give it a name (e.g., "NCD Chatbot")
4. Click **"Submit"**
5. **Copy your API key immediately** - you won't be able to see it again!

### Step 3: Add to Your Project
1. Open your `.env` file in the project root
2. Replace `your_groq_api_key_here` with your actual API key:

```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

3. Save the file

---

## Available Models

The project now uses **Llama 3.1 8B Instant** by default, but you can choose from:

| Model | Context Window | Best For |
|-------|---------------|----------|
| `llama-3.1-8b-instant` | 128K tokens | **Default** - Fast, balanced |
| `llama-3.1-70b-versatile` | 128K tokens | More accurate, versatile |
| `mixtral-8x7b-32768` | 32,768 tokens | Long conversations |
| `gemma2-9b-it` | 8,192 tokens | Google's Gemma 2 |

To change the model, update your `.env` file:

```env
GROQ_MODEL=llama-3.1-70b-versatile
```

Or modify the default in [src/chatbot.py](src/chatbot.py#L18)

---

## Testing Your Setup

### 1. Start the Backend
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run the server
python app.py
```

### 2. Test with Postman
Use the provided `POSTMAN_COLLECTION.json` to test the API endpoints.

### 3. Test with Frontend
```bash
cd ../my-chatbot-ui
npm run dev
```

---

## Troubleshooting

### "GROQ_API_KEY not found"
- Make sure your `.env` file is in the project root
- Check that the key name is exactly `GROQ_API_KEY`
- Restart your server after updating `.env`

### "Rate limit exceeded"
- Groq free tier: 30 req/min, 14,400 req/day
- Wait a minute or upgrade your plan at [Groq Pricing](https://groq.com/pricing/)

### "Invalid API key"
- Double-check you copied the entire key
- Create a new key if needed at [console.groq.com/keys](https://console.groq.com/keys)

---

## Resources

- [Groq Documentation](https://console.groq.com/docs/quickstart)
- [Groq Playground](https://console.groq.com/playground) - Test models in browser
- [Groq API Status](https://status.groq.com/) - Check service health

---

**Note:** Your API key is sensitive! Never commit your `.env` file to version control. The `.gitignore` already excludes it.
