# Bachelor's Thesis Landing Page

This repository contains the landing page for my bachelor's thesis project: "Development of Task Management API with JWT Authentication".

## Project Structure

```
landing-page/
├── css/
│   └── styles.css
├── img/
│   ├── favicon/
│   │   ├── android-chrome-192x192.png
│   │   ├── android-chrome-512x512.png
│   │   ├── apple-touch-icon.png
│   │   ├── favicon-16x16.png
│   │   └── favicon-32x32.png
│   ├── hero-image.svg
│   ├── methodology-diagram.svg
│   ├── og-image.jpg
│   └── university-logo.svg
├── files/
│   └── thesis.pdf
├── index.html
├── en.html
├── robots.txt
├── sitemap.xml
├── site.webmanifest
└── README.md
```

## Getting Started

1. Clone this repository:
```bash
git clone https://github.com/your-username/thesis-landing-page.git
cd thesis-landing-page
```

2. Open `index.html` in your browser to view the landing page locally.

## Deployment to GitHub Pages

This project is set up to be deployed to GitHub Pages automatically from the `main` branch.

To deploy manually:

1. Go to your repository on GitHub
2. Navigate to Settings > Pages
3. Select "main" branch as the source
4. Click Save

Your site will be available at `https://your-username.github.io/thesis-landing-page/`

## Git Branching Strategy

This project follows the GitHub Flow branching strategy:

1. **Main Branch**: Always contains production-ready code
2. **Feature Branches**: Created for each new feature or change
   - Branch from `main`
   - Name format: `feature/descriptive-name`
3. **Pull Requests**: Used to merge features back to `main`
4. **Direct Deployment**: The `main` branch is automatically deployed

### Workflow Example

```bash
# Start a new feature
git checkout main
git pull
git checkout -b feature/add-projects-section

# Make changes and commit
git add .
git commit -m "Add projects section with demo links"

# Push feature branch to remote
git push -u origin feature/add-projects-section

# Create a Pull Request on GitHub
# After review and approval, merge to main

# Switch back to main and pull latest changes
git checkout main
git pull
```

## Development Stages

The development of this landing page followed these key stages:

1. **Initial Setup**:
   - Basic HTML structure
   - CSS reset and variables
   - Meta tags and SEO basics
   - Favicon and web manifest

2. **Accessibility & SEO**:
   - Semantic HTML elements
   - ARIA attributes
   - Alt text for images
   - Schema.org markup
   - Open Graph tags

3. **Content Implementation**:
   - Thesis title and description
   - Research objectives
   - Methodology section
   - Expected results
   - Contact information

4. **Styling & Responsiveness**:
   - Typography and color scheme
   - Responsive design for all screen sizes
   - Interactive elements
   - Print stylesheet

## License

This project is licensed under the MIT License - see the LICENSE file for details.
