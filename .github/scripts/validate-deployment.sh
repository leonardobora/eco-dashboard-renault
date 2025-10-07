#!/bin/bash
# Validation script for GitHub Pages deployment
# This script validates that all required files are present and properly configured

set -e

echo "================================"
echo "GitHub Pages Deployment Validator"
echo "================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Function to check file existence
check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅${NC} $description: $file"
        return 0
    else
        echo -e "${RED}❌${NC} $description: $file (MISSING)"
        ((ERRORS++))
        return 1
    fi
}

# Function to check content
check_content() {
    local file=$1
    local pattern=$2
    local description=$3
    
    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}✅${NC} $description"
        return 0
    else
        echo -e "${YELLOW}⚠️${NC}  $description (NOT FOUND)"
        ((WARNINGS++))
        return 1
    fi
}

echo "📁 Checking Required Files..."
echo "================================"

# Check HTML files
check_file "index.html" "Dashboard HTML"
check_file "sobre.html" "About page HTML"

# Check CSS
check_file "static/css/style.css" "Main stylesheet"

# Check JavaScript
check_file "static/js/app.js" "Main application JS"
check_file "static/js/metrics-calculator.js" "Metrics calculator JS"

# Check Jekyll configuration
check_file ".nojekyll" "Jekyll bypass file"

echo ""
echo "🔍 Checking HTML Structure..."
echo "================================"

if [ -f "index.html" ]; then
    check_content "index.html" "metrics-calculator.js" "Index includes metrics-calculator.js"
    check_content "index.html" "style.css" "Index includes style.css"
    check_content "index.html" "sobre.html" "Index has navigation to sobre.html"
    check_content "index.html" "EcoTI Dashboard" "Index has correct title"
fi

if [ -f "sobre.html" ]; then
    check_content "sobre.html" "style.css" "Sobre includes style.css"
    check_content "sobre.html" "index.html" "Sobre has navigation to index.html"
fi

echo ""
echo "🔧 Checking Workflow Configuration..."
echo "================================"

# Check GitHub Actions workflow
check_file ".github/workflows/static.yml" "GitHub Pages workflow"

if [ -f ".github/workflows/static.yml" ]; then
    check_content ".github/workflows/static.yml" "validate-and-deploy" "Workflow has validation job"
    check_content ".github/workflows/static.yml" "actions/configure-pages" "Workflow configures Pages"
    check_content ".github/workflows/static.yml" "actions/deploy-pages" "Workflow deploys to Pages"
fi

echo ""
echo "📊 Checking File Sizes..."
echo "================================"

if [ -f "index.html" ]; then
    SIZE=$(stat -f%z "index.html" 2>/dev/null || stat -c%s "index.html" 2>/dev/null)
    if [ $SIZE -gt 1000 ]; then
        echo -e "${GREEN}✅${NC} index.html size: $SIZE bytes"
    else
        echo -e "${YELLOW}⚠️${NC}  index.html size seems too small: $SIZE bytes"
        ((WARNINGS++))
    fi
fi

if [ -f "sobre.html" ]; then
    SIZE=$(stat -f%z "sobre.html" 2>/dev/null || stat -c%s "sobre.html" 2>/dev/null)
    if [ $SIZE -gt 1000 ]; then
        echo -e "${GREEN}✅${NC} sobre.html size: $SIZE bytes"
    else
        echo -e "${YELLOW}⚠️${NC}  sobre.html size seems too small: $SIZE bytes"
        ((WARNINGS++))
    fi
fi

echo ""
echo "================================"
echo "Validation Summary"
echo "================================"
echo -e "Errors: ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}❌ Validation FAILED${NC} - Please fix the errors above"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Validation PASSED with warnings${NC} - Consider reviewing warnings"
    exit 0
else
    echo -e "${GREEN}✅ Validation PASSED${NC} - All checks successful!"
    exit 0
fi
