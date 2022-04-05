# Algolia Search

## Run Locally
1. `docker compose up --build` This will run the app on `localhost:3000`
2. Go to data folder, and upload all of the test essays from Paul Graham.
3. Add parse configs to both text boxes in the UI.
```
{
    "delim" : "\\.", // Set delimiter
    "min_size": 200, // Minimum character length for a passage
    "ignore": "\\n" // Characters to ignore in index
}
```
4. You can now search indivdually on each panel.