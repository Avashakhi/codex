from setuptools import setup, find_packages

setup(
    name='codex_cli',  # Package name (with underscore)
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'google-generativeai',
        'Pillow',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'codex-cli=codex_cli.main:main',  # ✅ Corrected: points to codex_cli/main.py
        ],
    },
    author='Chinnapothula Akhil',
    author_email='your.email@example.com',
    description='A CLI tool powered by Google Gemini for various functionalities like code generation, explanation, etc.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/codex_cli',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
