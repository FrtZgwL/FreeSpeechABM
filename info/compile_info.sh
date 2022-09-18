echo "Converting info.tex to Markdown for README file..."
pandoc -s info.tex -o info.md
pandoc -s info.md why_am_i_doing_this.md -o ../README.md
echo "Compiling info.tex as a PDF..."
latexmk --lualatex info.tex