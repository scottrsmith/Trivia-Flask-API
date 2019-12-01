#m2r README.md README.rst --overwrite
cp -R README.rst ./docs/source
cd ./docs
make html
# Make pdf
make latexpdf
cd ..
cp -R ./docs/build/latex/triviaapi.pdf .
