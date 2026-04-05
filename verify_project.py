#!/usr/bin/env python
"""
WhatsApp Chat Analyzer - Deployment Helper
This script helps you test and prepare the project for deployment
"""

import sys
import os

def check_structure():
    """Verify project structure"""
    print("\n📁 Checking Project Structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'LICENSE',
        '.gitignore',
        'CONTRIBUTING.md',
        'QUICKSTART.md',
        'PROJECT_CHECKLIST.md',
        'src/__init__.py',
        'src/preprocessing.py',
        'src/feature_engineering.py',
        'src/analysis.py',
        'tests/__init__.py',
        'tests/test_analyzer.py',
        '.streamlit/config.toml',
        '.github/workflows/code-quality.yml',
        '.github/workflows/tests.yml',
        'data/sample_chat.txt',
        'assets/INSTALLATION_GUIDE.md',
    ]
    
    missing = []
    for file in required_files:
        path = os.path.join(os.path.dirname(__file__), file)
        if not os.path.exists(path):
            missing.append(file)
        else:
            print(f"  ✅ {file}")
    
    if missing:
        print(f"\n  ❌ Missing files: {missing}")
        return False
    else:
        print("\n✅ All project files present!")
        return True


def test_imports():
    """Test that all modules can be imported"""
    print("\n🔧 Testing Module Imports...")
    
    try:
        print("  • Importing preprocessing...", end=" ")
        from src.preprocessing import ChatPreprocessor
        print("✅")
        
        print("  • Importing feature_engineering...", end=" ")
        from src.feature_engineering import FeatureEngineer
        print("✅")
        
        print("  • Importing analysis...", end=" ")
        from src.analysis import ChatAnalyzer
        print("✅")
        
        print("  • Importing streamlit...", end=" ")
        import streamlit
        print("✅")
        
        print("\n✅ All imports successful!")
        return True
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        return False


def get_file_stats():
    """Print project statistics"""
    print("\n📊 Project Statistics...")
    
    root_dir = os.path.dirname(__file__)
    
    # Count Python files
    py_files = 0
    total_lines = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv']]
        
        for file in files:
            if file.endswith('.py'):
                py_files += 1
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                        total_lines += lines
                except:
                    pass
    
    print(f"  • Python files: {py_files}")
    print(f"  • Total lines of code: {total_lines:,}")
    print(f"  • Documentation files: README.md, INSTALLATION_GUIDE.md, QUICKSTART.md")
    print(f"  • Features extracted: 25+")
    print(f"  • Visualizations: 10+")


def print_github_instructions():
    """Print GitHub deployment instructions"""
    print("\n" + "="*60)
    print("🚀 GITHUB DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    
    instructions = """
1. INITIALIZE YOUR LOCAL GIT REPOSITORY:
   cd c:\\Users\\HP\\Desktop\\whatsappchat
   git init
   git add .
   git commit -m "Initial commit: WhatsApp Chat Analyzer"

2. CREATE GITHUB REPOSITORY:
   • Go to https://github.com/new
   • Create new repository: "whatsappchat"
   • Copy the repository URL
   • DO NOT initialize with README

3. CONNECT LOCAL TO REMOTE:
   git remote add origin https://github.com/YOUR_USERNAME/whatsappchat.git
   git branch -M main
   git push -u origin main

4. UPDATE DOCUMENTATION:
   • Edit README.md and replace placeholders:
     - "yourusername" → your GitHub username
     - Add your contact information
     - Add project screenshots (optional)

5. VERIFY GITHUB FEATURES:
   • Go to Settings > Actions
   • Verify CI/CD workflows are enabled
   • Make repository Public (if desired)
   • Enable Issues and Discussions

6. ADD TOPICS (OPTIONAL):
   • Go to Settings > About
   • Add topics: whatsapp, nlp, streamlit, data-analysis, visualization

7. ENABLE GITHUB PAGES (OPTIONAL):
   • Go to Settings > Pages
   • Select Source: Deploy from a branch
   • Branch: main, folder: /docs

COMMAND SHORTCUT (all in one):
   git init
   git add .
   git commit -m "Initial commit: WhatsApp Chat Analyzer Project"
   git remote add origin YOUR_REPO_URL
   git branch -M main
   git push -u origin main
"""
    print(instructions)


def main():
    """Run all checks"""
    print("="*60)
    print("📊 WhatsApp Chat Analyzer - Project Verification")
    print("="*60)
    
    structure_ok = check_structure()
    imports_ok = test_imports()
    get_file_stats()
    print_github_instructions()
    
    if structure_ok and imports_ok:
        print("\n" + "="*60)
        print("✅ PROJECT READY FOR GITHUB!")
        print("="*60)
        print("\nNext steps:")
        print("1. Follow the GitHub instructions above")
        print("2. Test the app locally: streamlit run app.py")
        print("3. Push to GitHub")
        print("4. Share your project! 🎉")
    else:
        print("\n⚠️ Project has issues. Please fix before deploying.")
        sys.exit(1)


if __name__ == "__main__":
    main()
