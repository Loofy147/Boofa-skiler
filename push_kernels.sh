export KAGGLE_API_TOKEN=KGAT_7972aa3c1ae3f10a452943afc4b51193

echo "🚀 Pushing v1..."
cp kernel-metadata-v1.json kernel-metadata.json
kaggle kernels push -p .

echo "🚀 Pushing v2..."
cp kernel-metadata-v2.json kernel-metadata.json
kaggle kernels push -p .

echo "🚀 Pushing v3..."
cp kernel-metadata-v3.json kernel-metadata.json
kaggle kernels push -p .

echo "🚀 Pushing TPU..."
cp kernel-metadata-tpu.json kernel-metadata.json
kaggle kernels push -p .
