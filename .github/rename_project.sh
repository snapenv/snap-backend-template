#!/usr/bin/env bash
while getopts a:n:u:d: flag
do
    case "${flag}" in
        a) author=${OPTARG};;
        n) name=${OPTARG};;
        u) urlname=${OPTARG};;
        d) description=${OPTARG};;
    esac
done

echo "Author: $author";
echo "Project Name: $name";
echo "Project URL name: $urlname";
echo "Description: $description";

echo "Renaming project..."

original_author="snapenv"
original_name="snap_backend_template"
original_urlname="snap-backend-template"
original_description="SnapEnv template for backend server."
# Iterate over all files in the repository
git ls-files | while read -r filename; do
    # Exclude .github/workflows/rename_project.yml from renaming
    if [[ "$filename" != ".github/workflows/rename_project.yml" ]]; then
        sed -i "s/$original_author/$author/g" "$filename"
        sed -i "s/$original_name/$name/g" "$filename"
        sed -i "s/$original_urlname/$urlname/g" "$filename"
        sed -i "s/$original_description/$description/g" "$filename"
        echo "Renamed $filename"
    else
        echo "Skipping $filename"
    fi
done

mv "src/$original_name" "src/$name"

# This command runs only once on GHA!
rm -rf .github/template.yml
