#!/bin/bash
#
# Create Git tags for versions listed in CHANGELOG.md
#
# Usage:
#   ./create_tags.sh                    # Interactive mode - prompts for each version
#   ./create_tags.sh --auto             # Auto mode - creates all tags without prompting
#   ./create_tags.sh --version 2.2.0    # Create tag for specific version only
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if CHANGELOG.md exists
if [ ! -f "CHANGELOG.md" ]; then
    print_error "CHANGELOG.md not found in current directory"
    exit 1
fi

# Parse command line arguments
AUTO_MODE=false
SPECIFIC_VERSION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --auto)
            AUTO_MODE=true
            shift
            ;;
        --version)
            SPECIFIC_VERSION="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --auto              Create all tags without prompting"
            echo "  --version VERSION   Create tag for specific version only"
            echo "  --help, -h          Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                    # Interactive mode"
            echo "  $0 --auto             # Create all tags automatically"
            echo "  $0 --version 2.2.0    # Create tag for version 2.2.0 only"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Extract versions from CHANGELOG.md
print_info "Extracting versions from CHANGELOG.md..."
VERSIONS=$(grep -oP '## Version \K[0-9]+\.[0-9]+\.[0-9]+' CHANGELOG.md)

if [ -z "$VERSIONS" ]; then
    print_error "No versions found in CHANGELOG.md"
    exit 1
fi

print_success "Found versions:"
echo "$VERSIONS" | while read -r version; do
    echo "  - $version"
done
echo ""

# Get current commit SHA
CURRENT_COMMIT=$(git rev-parse HEAD)
print_info "Current commit: $CURRENT_COMMIT"
echo ""

# Check if we're on a clean working directory
if ! git diff-index --quiet HEAD --; then
    print_warning "Working directory has uncommitted changes"
    if [ "$AUTO_MODE" = false ]; then
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Aborted"
            exit 1
        fi
    fi
fi

# Function to create a tag
create_tag() {
    local version=$1
    local tag_name="v${version}"
    
    # Check if tag already exists
    if git rev-parse "$tag_name" >/dev/null 2>&1; then
        print_warning "Tag $tag_name already exists, skipping"
        return 1
    fi
    
    # Create the tag
    print_info "Creating tag $tag_name..."
    if git tag -a "$tag_name" -m "Release version $version" 2>/dev/null; then
        print_success "Created tag $tag_name"
        return 0
    else
        print_error "Failed to create tag $tag_name"
        return 1
    fi
}

# Process versions
CREATED_TAGS=()
SKIPPED_TAGS=()

if [ -n "$SPECIFIC_VERSION" ]; then
    # Create tag for specific version only
    if echo "$VERSIONS" | grep -q "^${SPECIFIC_VERSION}$"; then
        if create_tag "$SPECIFIC_VERSION"; then
            CREATED_TAGS+=("v${SPECIFIC_VERSION}")
        else
            SKIPPED_TAGS+=("v${SPECIFIC_VERSION}")
        fi
    else
        print_error "Version $SPECIFIC_VERSION not found in CHANGELOG.md"
        exit 1
    fi
else
    # Process all versions
    echo "$VERSIONS" | while read -r version; do
        if [ "$AUTO_MODE" = false ]; then
            read -p "Create tag v${version}? (y/N) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_warning "Skipped v${version}"
                continue
            fi
        fi
        
        if create_tag "$version"; then
            CREATED_TAGS+=("v${version}")
        else
            SKIPPED_TAGS+=("v${version}")
        fi
    done
fi

# Summary
echo ""
print_info "Summary:"
if [ ${#CREATED_TAGS[@]} -gt 0 ]; then
    print_success "Created ${#CREATED_TAGS[@]} tag(s)"
    for tag in "${CREATED_TAGS[@]}"; do
        echo "  - $tag"
    done
fi

if [ ${#SKIPPED_TAGS[@]} -gt 0 ]; then
    print_warning "Skipped ${#SKIPPED_TAGS[@]} tag(s)"
    for tag in "${SKIPPED_TAGS[@]}"; do
        echo "  - $tag"
    done
fi

# Prompt to push tags
if [ ${#CREATED_TAGS[@]} -gt 0 ]; then
    echo ""
    if [ "$AUTO_MODE" = false ]; then
        read -p "Push tags to origin? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Pushing tags to origin..."
            if git push origin --tags; then
                print_success "Tags pushed successfully"
            else
                print_error "Failed to push tags"
                exit 1
            fi
        else
            print_info "Tags created locally but not pushed"
            print_info "To push later, run: git push origin --tags"
        fi
    else
        print_info "Auto mode: To push tags, run: git push origin --tags"
    fi
fi

print_success "Done!"
