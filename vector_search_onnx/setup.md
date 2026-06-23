1. setup environment
mkdir llm-zoomcamp-onnx && cd llm-zoomcamp-onnx
uv init --no-workspace
uv add onnxruntime tokenizers numpy tqdm minsearch
uv add --dev huggingface-hub jupyter

uv run python -m ipykernel install --user --name llm-zoomcamp-onnx --display-name "llm-zoomcamp-onnx"

2. Download and run download.py

wget https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/d71d4a43e12b23e8a3c0441b831217bd6f41e454/02-vector-search/embed/download.py

uv run python download.py

3. Add the models directory to .gitignore

4. Download embedder.py

wget https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/refs/heads/main/02-vector-search/embed/embedder.py

5. Download ingest.py

wget https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/01-agentic-rag/code/ingest.py

6. To use a different model, add it to download.py, run the download, then update the path:

embed = Embedder("models/Xenova/bge-base-en-v1.5")
vectors = embed.encode("your text here")
print(vectors.shape)