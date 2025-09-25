#!/usr/bin/env python
import warnings
import gradio as gr
from sp.crew import Sp
from sp.crew import JurySp
import traceback
import litellm
import httpx

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run_pitch_battle(startup_name, industry, mission, product, target_market, funding_stage):
    """
    Run the crew.
    """

    inputs = {
        "name": startup_name,
        "industry": industry,
        "mission": mission,
        "product": product,
        "target_market": target_market,
        "initial_funding": funding_stage,
        "variation": 1,
    }

    plugin_map = {
        "fnb": "You are a veteran with 30 years in the food & beverage industry.",
        "healthcare": "You are a healthcare industry executive with 25 years of experience."
    }

    industry = inputs["industry"].lower()
    plugin_context = plugin_map.get(industry, "")
    inputs['plugin_context'] = plugin_context

    outputs = [""] * 8

    try:
        crew = Sp().crew();
        for step, data in crew.kickoff(inputs=inputs):
            if data is None:
                continue

            if step == "tasks_output" and isinstance(data, list):
                _assign_task_outputs(data, outputs, offset=0)
                yield tuple(outputs)

        inputs['variation'] = 2
        for step, data in crew.kickoff(inputs=inputs):
            if data is None:
                continue

            if step == "tasks_output" and isinstance(data, list):
                _assign_task_outputs(data, outputs, offset=3)
                yield tuple(outputs)

        jury_inputs = {
            "startup": startup_name,
            "variation_1_pitch": outputs[0],
            "variation_1_financials": outputs[1],
            "variation_1_engineering": outputs[2],
            "variation_2_pitch": outputs[3],
            "variation_2_financials": outputs[4],
            "variation_2_engineering": outputs[5],
        }


        for step, data in JurySp().crew().kickoff(inputs=jury_inputs):
            if step == "tasks_output" and isinstance(data, list):
                for task_output in data:
                    if task_output.name == "evaluation_task":
                        outputs[6] = task_output.raw
                yield tuple(outputs)
    except (litellm.exceptions.InternalServerError, httpx.HTTPStatusError) as e:
        msg = (
            "⚠️ The AI model is currently overloaded (503 Service Unavailable). "
            "Please try again in a few seconds."
        )
        outputs[-1] = msg
        yield tuple(outputs)
    except Exception as e:
        tb = traceback.format_exc()
        yield ("", "", "", "", "", "", "", f"❌ Error:\n```\n{tb}\n```")


def _assign_task_outputs(data, outputs, offset=0):
    """Helper to assign crew task outputs to the correct slots in outputs list."""
    for task_output in data:
        if not hasattr(task_output, "name"):
            continue

        if task_output.name == "pitch_task":
            outputs[offset] = task_output.raw
        elif task_output.name == "financial_task":
            outputs[offset + 1] = task_output.raw
        elif task_output.name == "engineering_task":
            outputs[offset + 2] = task_output.raw


def set_in_progress(*args):
    return gr.update(value="""
    <div style="display:flex;align-items:center;gap:8px;">
        <div class="loader"></div>
        <span>⏳ Running pitch battle...</span>
    </div>
    <style>
        .loader {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #3498db;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """)

def update_status(errors):
    if errors.strip():
        return "❌ See Errors tab ❌"
    return ""

def disable_button(*args):
    return gr.update(interactive=False)

def enable_button(*args):
    return gr.update(interactive=True)

def validate_inputs(startup_name, industry, mission, product, target_market, funding_stage):
    missing = []
    if not startup_name.strip():
        missing.append("Startup Name")
    if not industry.strip():
        missing.append("Industry")
    if not mission.strip():
        missing.append("Mission")
    if not product.strip():
        missing.append("Product")
    if not target_market.strip():
        missing.append("Target Market")
    if not funding_stage.strip():
        missing.append("Funding Stage")

    if missing:
        raise gr.Error(f"❌ Missing required fields: {', '.join(missing)}")

preset_startups = {
    "Hospitality": {
        "name": "StaySmart",
        "industry": "Hospitality",
        "mission": "Affordable smart hotel experiences",
        "product": "AI-powered booking and room automation platform",
        "target_market": "Business travelers and digital nomads",
        "initial_funding": "Seed, $1.5M"
    },
    "Mobile App": {
        "name": "FitTrack",
        "industry": "Software",
        "mission": "Gamify fitness and personal health goals",
        "product": "Mobile app with AI-coaching and wearable sync",
        "target_market": "Health-conscious millennials",
        "initial_funding": "Series A, $5M"
    },
    "Coffee Shop": {
        "name": "Veronika's Coffee Palace",
        "industry": "Food & Beverage",
        "mission": "Redefine the coffeehouse experience by blending tradition with innovation.",
        "product": "AI-powered tools and services to enhance customer engagement and streamline operations.",
        "target_market": "Young professionals and students seeking convenience and quality.",
        "initial_funding": "Seed Round - $800,000",
    },
    "Manufacturing": {
        "name": "RoboFab",
        "industry": "Manufacturing",
        "mission": "Automated small-scale production for SMEs",
        "product": "Robotics-based flexible manufacturing line",
        "target_market": "Small to mid-sized manufacturers",
        "initial_funding": "Series B, $15M"
    }
}

common_industries = [
    "Food & Beverage",
    "Hospitality",
    "Healthcare",
    "Fintech",
    "Education",
    "Manufacturing",
    "Green Energy",
    "Retail & E-Commerce",
    "Transportation & Mobility",
    "Entertainment & Media",
    "Real Estate & PropTech",
    "Software",
    "Other"
]

with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🚀 Startup Pitch Variations Battle")

    status = gr.HTML("")

    with gr.Row():
        with gr.Column(scale=2):
            startup_name = gr.Textbox(label="Startup Name", placeholder="Your startup name")
            industry = gr.Dropdown(label="Industry", choices=common_industries, value="Other", interactive=True)
            mission = gr.Textbox(label="Mission", placeholder="Affordable EV charging")
            product = gr.Textbox(label="Product", placeholder="Solar panels + AI load-balancer")
            target_market = gr.Textbox(label="Target Market", placeholder="Urban commuters")
            funding_stage = gr.Textbox(label="Funding Stage", placeholder="Seed, $2M")

            run_button = gr.Button("🔥 Run")

        with gr.Column(scale=2):
            gr.Markdown("### 💡 Try Preset Startup Ideas")
            with gr.Row():
                for idea_name, idea in preset_startups.items():
                    gr.Button(idea_name).click(
                        lambda i=idea: (i["name"], i["industry"], i["mission"], i["product"], i["target_market"], i["initial_funding"]),
                        inputs=[],
                        outputs=[startup_name, industry, mission, product, target_market, funding_stage]
                    )

            with gr.Tabs():
                with gr.Tab("Variation 1"):
                    with gr.Tabs():
                        with gr.Tab("Pitch"):
                            v1_pitch = gr.Markdown()
                        with gr.Tab("Financials"):
                            v1_financial = gr.Markdown()
                        with gr.Tab("Tech"):
                            v1_engineering = gr.Markdown()

                with gr.Tab("Variation 2"):
                    with gr.Tabs():
                        with gr.Tab("Pitch"):
                            v2_pitch = gr.Markdown()
                        with gr.Tab("Financials"):
                            v2_financial = gr.Markdown()
                        with gr.Tab("Tech"):
                            v2_engineering = gr.Markdown()

                with gr.Tab("Jury Verdict"):
                    verdict = gr.Markdown()

                with gr.Tab("Errors"):
                    errors = gr.Markdown()

    run_button.click(
        fn=disable_button,
        inputs=[startup_name, industry, mission, product, target_market, funding_stage],
        outputs=[run_button]
    ).then(
        fn=validate_inputs,
        inputs=[startup_name, industry, mission, product, target_market, funding_stage],
        outputs=None
    ).then(
        fn=set_in_progress,
        inputs=[startup_name, industry, mission, product, target_market, funding_stage],
        outputs=[status]
    ).then(
        fn=run_pitch_battle,
        inputs=[startup_name, industry, mission, product, target_market, funding_stage],
        outputs=[v1_pitch, v1_financial, v1_engineering,
                v2_pitch, v2_financial, v2_engineering,
                verdict, errors]
    ).then(
        fn=enable_button,
        inputs=[],
        outputs=[run_button]
    ).then(
        fn=update_status,
        inputs=[errors],
        outputs=[status]
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=5002)
