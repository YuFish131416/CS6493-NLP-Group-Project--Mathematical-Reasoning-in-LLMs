"""
Interactive Math Problem Solver page.
Users can input a math problem, select a model and prompt method,
and see the model's response with extracted answer.
"""

import sys
import os
import time

import streamlit as st

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

st.set_page_config(page_title="Interactive Solver", page_icon="✏️", layout="wide")
st.title("✏️ Interactive Math Problem Solver")
st.markdown("Enter a math problem and select a model + prompting method to see the result.")

# --- Input Section ---
col1, col2 = st.columns([2, 1])

with col1:
    problem_text = st.text_area(
        "Math Problem",
        value="Find the value of x if 3x + 7 = 22.",
        height=120,
        help="Enter any math problem you want to solve.",
    )

with col2:
    st.markdown("### Configuration")
    model_choice = st.selectbox(
        "Model",
        options=["qwen2.5-math", "deepseek-r1", "gpt-4o-mini", "deepseek-chat"],
        help="Select the model to use for inference.",
    )
    method_choice = st.selectbox(
        "Prompt Method",
        options=["cot", "self_consistency", "self_refine", "least_to_most", "pvp"],
        help="Select the prompting strategy.",
    )
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1)

solve_btn = st.button("🚀 Solve", type="primary", use_container_width=True)

# --- Result Section ---
if solve_btn:
    if not problem_text.strip():
        st.error("Please enter a math problem.")
    else:
        with st.spinner(f"Running {model_choice} with {method_choice}..."):
            try:
                # Load model and prompt method
                from src.prompts import CoT, SelfConsistency, SelfRefine, LeastToMost, PVP
                from src.models.router import ModelRouter
                import yaml
                from dotenv import load_dotenv

                load_dotenv()

                # Load config
                config_path = "config/config.local.yaml"
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        full_config = yaml.safe_load(f)
                else:
                    st.warning(
                        "config/config.local.yaml not found. "
                        "Using default settings. Copy config.example.yaml to config.local.yaml."
                    )
                    full_config = {"models": {}}

                # Initialize router
                router = ModelRouter(full_config)

                # Initialize prompt method
                method_map = {
                    "cot": CoT,
                    "self_consistency": SelfConsistency,
                    "self_refine": SelfRefine,
                    "least_to_most": LeastToMost,
                    "pvp": PVP,
                }
                prompt_method = method_map[method_choice]()
                prompt = prompt_method.format(problem=problem_text)

                # Display the formatted prompt
                with st.expander("📝 Formatted Prompt", expanded=False):
                    st.code(prompt, language="text")

                # Run inference
                start = time.time()
                response = router.infer(
                    prompt=prompt,
                    model_name=model_choice,
                    temperature=temperature,
                    max_tokens=2048,
                )
                elapsed = time.time() - start

                # Extract answer
                from src.evaluation.answer_extractor import extract_answer
                extracted = extract_answer(response)

                # Display results
                st.success(f"Response generated in {elapsed:.1f}s")

                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Extracted Answer", extracted or "Could not extract")
                with col_b:
                    st.metric("Response Length", f"{len(response)} characters")

                st.markdown("### Model Response")
                st.markdown(response)

            except FileNotFoundError as e:
                st.error(f"Model not found: {e}")
                st.info(
                    "Make sure you have downloaded the GGUF model files. "
                    "See README.md for download instructions."
                )
            except ValueError as e:
                st.error(f"Configuration error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# --- Sample Problems ---
st.markdown("---")
st.markdown("### Sample Problems")
sample_problems = [
    ("Algebra", "Find the value of x if 3x + 7 = 22."),
    ("Geometry", "A right triangle has legs of length 5 and 12. Find the length of the hypotenuse."),
    ("Number Theory", "What is the remainder when 2^100 is divided by 7?"),
    ("Combinatorics", "How many ways can 5 students be arranged in a line?"),
    ("Arithmetic", "If a shirt originally costs $40 and is on sale for 25% off, what is the sale price?"),
]

cols = st.columns(3)
for i, (category, prob) in enumerate(sample_problems):
    with cols[i % 3]:
        st.markdown(f"**{category}**")
        st.code(prob, language="text")
        if st.button(f"Use", key=f"sample_{i}", use_container_width=True):
            st.rerun()
