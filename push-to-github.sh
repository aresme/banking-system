#!/bin/bash
# Script to push to GitHub

echo "🏦 Banking System - GitHub Setup"
echo "================================"
echo ""
echo "This script will help you push the banking system to GitHub."
echo ""
echo "Prerequisites:"
echo "1. Create a new repository on GitHub at https://github.com/new"
echo "2. Name the repository: banking-system"
echo "3. Keep it public (optional)"
echo ""
echo "Steps to follow:"
echo ""
echo "Step 1: Copy your GitHub repository URL"
echo "        It should look like: https://github.com/YOUR_USERNAME/banking-system.git"
echo "        Or: git@github.com:YOUR_USERNAME/banking-system.git"
echo ""
read -p "Enter your GitHub repository URL: " GITHUB_URL
echo ""

# Add remote
echo "Step 2: Adding remote repository..."
git remote add origin "$GITHUB_URL"

# Verify remote was added
echo "Verifying remote..."
git remote -v

# Create main branch and push
echo ""
echo "Step 3: Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Success! Your repository is now on GitHub"
echo ""
echo "You can view it at: $GITHUB_URL"
