# automated-protein-interaction-labeler
A mcp-server to generate effective prompts for llm-assisted protein-protein interaction analysis.
This project explores a smarter approach to protein complex analysis by employing Large Language Models (LLMs) for automated annotation. Our server processes protein structures from PDB files, supporting T-cell receptor (TCR) and peptide-MHC (pMHC) complex interactions to automatically identify chain types and generate quantitative labelings. Through optimized prompting techniques, our pipeline effectively mitigates LLM hallucination, ensuring high reliability.
## Core Capabilities
- ### Automated Chain Identification: Read Header in PDB file for chain classification
- ### Comprehensive Interaction Analysis: 
  - Hydrogen bond networks
  - Salt bridges
  - Hydrophobic interactions
  - π-π stacking interactions
  - Interface SASA calculations
  - Binding angle measurements
- ### Batch Processing: Analyze multiple PDB files with progress tracking
- ### Data Integrity: Real-time data collection and verification system

## Requirements
- Python 3.8+
- PyMOL (with Python API)
- Claude Desktop 
- MCP (Model Context Protocol) server framework
- MCP Server Plugins ：pymol-mcp-server, filesystem-mcp-server

## Quick start
### Installnation
### Pymol-mcp-server
For more detailed informations and server, click this link https://github.com/ChatMol/molecule-mcp
1. Go to Claude > Settings > Developer > Edit Config > claude_desktop_config.json to include the following:
{
  "mcpServers": {
    "pymol": {
      "command": "/path/to/mcp",
      "args": [
        "run",
        "/path/to/molecule-mcp/pymol_server.py"
      ]
     }
  }
}
2. Install mcp and get the script
pip install "mcp[cli]" chatmol
which mcp


Copy this path for the next step and replace /path/to/mcp with the path to mcp.
3. To get the path to molecule-mcp.
'''
git clone https://github.com/ChatMol/molecule-mcp.git
cd molecule-mcp
pwd
'''
the path to molecule-mcp will be displayed. Copy this path for the next step and replace /path/to/molecule-mcp with the path to molecule-mcp.

filesystem-mcp-server
1. Download Node.js     https://nodejs.org/zh-cn
   [图片]
