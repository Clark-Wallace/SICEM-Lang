import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sicem_lang",
    version="0.1.0",
    author="Development Team",
    author_email="",
    description="CI-aware Slang CLI and toolkit for AI communication sessions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    # Include the Toolbox package and all top-level modules
    packages=setuptools.find_packages(include=["Toolbox", "Toolbox.*"]),
    py_modules=[
        "ai_interface",
        "cil_tracker",
        "gui_styles",
        "openai_interface",
        "session_manager",
        "signal_transmitter",
        "slang_assistant",
        "slang_assistant_gui",
        "slang_cli",
        "slang_gui",
        "slang_interpreter",
        "slang_parser",
        "slang_receive_cli",
        "slang_receiver",
        "slang_runner",
        "slang_session_cli",
        "slang_upload_cli",
        "slang_uploader",
        "slang_validate_cli",
    ],
    install_requires=[
        "pyyaml>=6.0.1",
        "typing-extensions>=4.5.0",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0"
    ],
    entry_points={
        'console_scripts': [
            'slang-upload=slang_upload_cli:main',
            'slang-receive=slang_receive_cli:main',
            'slang-session=slang_session_cli:main',
            'slang-validate=slang_validate_cli:main'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)