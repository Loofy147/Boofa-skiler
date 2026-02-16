#!/bin/bash
# 📦 Boofa-Med Submission Bundler

SUBMISSION_DIR="medgemma_submission"
mkdir -p $SUBMISSION_DIR/code/competitions/medgemma
mkdir -p $SUBMISSION_DIR/code/layers/layer_1_domain
mkdir -p $SUBMISSION_DIR/code/layers/layer_2_core
mkdir -p $SUBMISSION_DIR/code/layers/layer_3_optimization
mkdir -p $SUBMISSION_DIR/code/layers/layer_4_discovery
mkdir -p $SUBMISSION_DIR/docs

echo "📦 Bundling Boofa-Med Submission..."

# Copy Competition Materials
cp competitions/medgemma/*.md $SUBMISSION_DIR/
cp competitions/medgemma/*.py $SUBMISSION_DIR/code/competitions/medgemma/
cp competitions/medgemma/Procfile $SUBMISSION_DIR/ || true

# Copy Core Logic
cp layers/layer_1_domain/medical_impact_core.py $SUBMISSION_DIR/code/layers/layer_1_domain/
cp layers/layer_1_domain/medical_realizations.json $SUBMISSION_DIR/code/layers/layer_1_domain/
cp layers/layer_2_core/realization_engine.py $SUBMISSION_DIR/code/layers/layer_2_core/
cp layers/layer_3_optimization/medical_ethics_auditor.py $SUBMISSION_DIR/code/layers/layer_3_optimization/
cp layers/layer_4_discovery/clinical_delta_engine.py $SUBMISSION_DIR/code/layers/layer_4_discovery/

# Copy Environment/Config
cp requirements.txt $SUBMISSION_DIR/

# Rename writeup for clarity
mv $SUBMISSION_DIR/writeup_draft.md $SUBMISSION_DIR/FINAL_WRITEUP.md

echo "✅ Bundle Complete: $SUBMISSION_DIR/"
ls -R $SUBMISSION_DIR/
