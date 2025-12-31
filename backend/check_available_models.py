#!/usr/bin/env python3
"""
Check available Gemini models for your API key.
"""

import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import settings

def check_available_models():
    """Check what models are available for your API key."""
    print("🔍 Checking available Gemini models...")
    print("=" * 50)

    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.google_api_key)

        print("✅ Connected to Gemini API")
        print()

        # List available models
        models = genai.list_models()
        print("📋 Available models:")

        text_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                model_name = model.name.replace('models/', '')
                text_models.append(model_name)
                print(f"   ✅ {model_name}")
                print(f"      Display name: {model.display_name}")
                print(f"      Description: {model.description}")
                print(f"      Input token limit: {model.input_token_limit}")
                print(f"      Output token limit: {model.output_token_limit}")
                print()

        if not text_models:
            print("❌ No text generation models found!")
            return None

        # Recommend the best model
        recommended_models = ['gemini-pro', 'gemini-1.5-flash', 'gemini-1.5-pro-latest']
        recommended = None

        for model in recommended_models:
            if model in text_models:
                recommended = model
                break

        if recommended:
            print(f"🎯 Recommended model: {recommended}")
        else:
            print(f"🎯 Using first available model: {text_models[0]}")
            recommended = text_models[0]

        return recommended

    except Exception as e:
        print(f"❌ Error checking models: {str(e)}")
        return None

if __name__ == "__main__":
    recommended_model = check_available_models()

    if recommended_model:
        print(f"\n💡 Update your .env file with:")
        print(f"GEMINI_MODEL={recommended_model}")
        print(f"\nOr run this command to update it:")
        print(f"sed -i 's/GEMINI_MODEL=.*/GEMINI_MODEL={recommended_model}/' .env")