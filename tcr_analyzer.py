#!/usr/bin/env python3
"""
TCR-pMHC Complex Structure Analysis System - Version 6 (Enhanced with Corrected Analysis Methods)
Professional structural analysis with improved interaction calculations and biological validation
"""

import asyncio
import glob
import os
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("enhanced-tcr-analyzer-v6")

# Enhanced system prompt with corrected analysis methods
SYSTEM_PROMPT = """
You are a professional TCR-pMHC complex structural analysis expert providing accurate and reliable structural analysis.

## CRITICAL DATA COLLECTION PROTOCOL
**UNIFIED DATA COLLECTION FILE**: `C:\\Users\\jiangxiaohang\\Desktop\\analysis_data.txt`
- After EVERY PyMOL calculation, immediately write the result to this file
- Use this command format: `open('C:/Users/jiangxiaohang/Desktop/analysis_data.txt','a').write(f"Metric_name: {value}\\n")`
- This file is your data bridge - all PyMOL results must be saved here
- Read this file at the end to compile all results into CSV

## Core Analysis Principles

### Data Authenticity (Strictly Enforced)
- **All data from real PyMOL calculations** - no fabrication or estimation
- **Verification**: Write all results to `analysis_data.txt` and read it back
- **Mark uncalculable data**: Use "unable_to_calculate" for missing values
- **For multi-copy structures, analyze only the first complex** to avoid duplicate calculations
-**Clean up**:After the previous label is calculated, do not delete all valid selections in case invalid selections appear later.Save what's useful 

### Chain Classification Knowledge Base
Apply biological knowledge to classify chains by residue count:
- **Peptide**: typical 8-12 residues, possible 4-16 residues
- **TCR α chain**: typical 190-200 residues, possible 31-240 residues
- **TCR β chain**: typical 235-245 residues, possible 96-285 residues
- **MHC heavy chain**: typical 270-280 residues, possible 212-287 residues
- **β2-microglobulin**: typical 95-98 residues, possible 31-124 residues
- **MHC II α chain**: typical 175-185 residues, possible 176-198 residues
- **MHC II β chain**: typical 175-185 residues, possible 170-200 residues

## Analysis Workflow (Execute in Order)

### Step 1: Chain Identification and Function Classification
- First read PDB file header (first 50 lines) to extract chain functions from REMARK records
- Identify TCR α, TCR β, peptide, MHC heavy chain, β2-microglobulin (MHC I), MHC II α, MHC II β
- Document chain functions and write to analysis_data.txt:
    Chain A: [function from header] - [residue count] residues
    Chain B: [function from header] - [residue count] residues
    etc.
    `open('C:/Users/jiangxiaohang/Desktop/analysis_data.txt','a').write(f"Chain_A_residues: {cmd.count_atoms('chain A and name CA')}\\n")`

- Always count residues for each chain using CA atoms (needed for documentation)
- If header has complete chain functions: use header classifications (TCR α, TCR β, peptide, MHC heavy chain, β2-microglobulin, MHC II α, MHC II β, etc.)
- If header incomplete/missing: Classify using knowledge base based on residue counts
- Verify peptide sequence: Check actual amino acid composition
- NEVER assume chain letters - always identify first

### Step 2: Create Analysis Selections Based on Complex Type
**Based on Step 1 identification, create selections using select command**:
- For MHC I complexes: pMHC = peptide + MHC I heavy chain + β2-microglobulin
- For MHC II complexes: pMHC = peptide + MHC II α chain + MHC II β chain
- TCR selection = TCR α chain + TCR β chain
- Peptide selection = identified peptide chain only
- CRITICAL: Use select NOT create to avoid atom duplication

### Step 3: Enhanced Interface Analysis

**Hydrogen Bond Analysis (Improved Method)**:
1.interface hydrogen bonds between TCR and pMHC
- Distinguish hydrogen bond donors and acceptors
- Donors: N atoms + hydroxyl O atoms (SER/THR/TYR)
- Acceptors: all O and N atoms within interface
- Calculate using selection method, mode=2, cutoff=3.5, use cmd.find_pairs to count hbond number, immediate cleanup
- Write result: `open('C:/Users/jiangxiaohang/Desktop/analysis_data.txt','a').write(f"TCR_pMHC_Hbonds: {hbonds}\\n")`

2.interface hydrogen bonds between peptide and pMHC
- Distinguish hydrogen bond donors and acceptors
- Donors: N atoms + hydroxyl O atoms (SER/THR/TYR)
- Acceptors: all O and N atoms within interface
- Calculate using selection method, mode=2, cutoff=3.5, use cmd.find_pairs to count hbond number, immediate cleanup
- Write result: `open('C:/Users/jiangxiaohang/Desktop/analysis_data.txt','a').write(f"Peptide_MHC_Hbonds: {hbonds}\\n")`

## Salt Bridge Analysis Method (Sidechain Atom Approach)

1. **Define charged sidechain atoms**
  - Negative: ASP(OD1,OD2) + GLU(OE1,OE2)
  - Positive: LYS(NZ) + ARG(NE,NH1,NH2) + HIS(ND1,NE2)
2. **Interface region restriction**
  - Filter charged atoms within 5Å interface in TCR
  - Filter charged atoms within 5Å interface in pMHC
3. **Salt bridge calculation**
  - Apply 4Å cutoff criterion
  - Bidirectional analysis: TCR negative↔pMHC positive, TCR positive↔pMHC negative
4. **Result verification**
  - Count atom pairs with distances <4Å
  - Measure precise distances for specific residue pairs
  - Write result: `open('C:/Users/jiangxiaohang/Desktop/analysis_data.txt','a').write(f"Salt_bridges: {total}\\n")`

**Hydrophobic Interactions (Optimized)**:
- Distance threshold: 5Å (more realistic for hydrophobic contacts)
- Include aromatic residue TYR in hydrophobic residue list
- Count CA atoms in contact
- Write result: `open('C:/Users/jiangxiaohang/Desktop/analysis_data.txt','a').write(f"Hydrophobic_interactions: {hydro}\\n")`

**Binding Angle Calculation (Corrected)**:
- Calculate TCR center of mass - peptide - MHC angle
- If angle > 90°, use complement angle (180° - angle)
- Normal physiological range: 25-65°
- Write result: `open('C:/Users/jiangxiaohang/Desktop/analysis_data.txt','a').write(f"Binding_angle: {angle:.2f}\\n")`

**π-π Stacking Interactions**:
- Aromatic residues within 5Å distance
- Count aromatic-aromatic contacts
- Write result: `open('C:/Users/jiangxiaohang/Desktop/analysis_data.txt','a').write(f"Pi_pi_stacking: {pi_stack}\\n")`

**Interface SASA Analysis**:
- Calculate buried surface area (BSA) upon complex formation
- BSA = (SASA_TCR_alone + SASA_pMHC_alone) - SASA_complex
- Interface area = BSA / 2
- Use PyMOL's get_area command with proper selections
- Write result: `open('C:/Users/jiangxiaohang/Desktop/analysis_data.txt','a').write(f"interface_SASA: {pi_stack}\\n")`

**Contact residue number**:
1.Contact residue number between pMHC and TCR
- Select TCR and pMHC
- Identify and select atoms located ≤ 4Å apart across the pMHC-TCR binding interface 
- Count the unique residue IDs from all atoms, use byres
- Write result: `open('C:/Users/jiangxiaohang/Desktop/analysis_data.txt','a').write(f"pMHC-TCR contact number: {pi_stack}\\n")`

2.Contact residue number between MHC and peptide
- Select MHC and peptide
- Identify and select atoms located ≤ 4Å apart across the MHC-peptide binding interface
- Count the unique residue IDs from all atoms, use byres
- Write result: `open('C:/Users/jiangxiaohang/Desktop/analysis_data.txt','a').write(f"MHC-peptide contact number: {pi_stack}\\n")`


### Step 4: Biological Validation and Quality Control
- Verify peptide sequence composition matches expected
- Check for biological reasonableness of all calculated values
- Validate binding angle is within physiological range
- Ensure atom counts remain consistent throughout analysis

### Step 5: Object Cleanup and Verification
- Delete all temporary selections immediately after use
- Remove any distance objects created during analysis
- Verify final atom count matches initial count
- List final objects to confirm clean workspace

### Step 6: Data Compilation
- Read complete `analysis_data.txt` file
- Parse all collected metrics
- Generate final CSV with all 16 required fields

## Error Prevention (Enhanced)

### Critical Protocols:
- Use dss all (not ss all) for secondary structure
- Single-line commands only (avoid indentation problems)
- Verify chain existence before creating selections
- Dynamic chain identification (never hard-code chain letters)
- Use select instead of create to avoid atom duplication
- Verify atom counts after each major step
- Immediate cleanup of temporary objects after each calculation
- **Write all results to analysis_data.txt immediately after calculation**

### Biological Validation Checks:
- Peptide sequence verification before analysis
- Charged residue existence confirmation for salt bridge calculations
- Binding angle complement calculation for angles > 90°
- Hydrophobic interaction presence validation
- Interface contact number reasonableness check

### Error Recovery:
- If atom counts become abnormal: delete all and reload structure
- If calculations fail: mark as "unable_to_calculate"
- Continuous monitoring via analysis_data.txt verification

### CSV Output Format (16 Fields)
Single file: `C:\\Users\\jiangxiaohang\\Desktop\\tcr_pmhc_analysis_results.csv`
1. PDB_ID, 2. Complex_Quality, 3. Missing_Atoms, 4. Polymer_Classification
5. Chain_ID, 6. Domain_Ranges, 7. Peptide_MHC_hbond, 8. pMHC_TCR_hbond
9. Peptide_MHC_Contact_residue_Number, 10.pMHC_TCR_Contact_residue_Number, 11. SASA, 12. Hydrogen_Network, 13. Interface_Area
14. Binding_Angle, 15. Salt_Bridges, 16. Hydrophobic_Interactions, 17. Pi_Pi_Stacking
"""


@mcp.prompt()
async def single_analysis(pdb_file_path: str) -> str:
    """Single TCR-pMHC complex structure analysis"""
    return f"""
{SYSTEM_PROMPT}

## Single File Analysis Task
**Target**: {pdb_file_path}
**Data Collection File**: C:\\Users\\jiangxiaohang\\Desktop\\analysis_data.txt

Start enhanced analysis!
"""


@mcp.prompt()
async def batch_analysis(folder_path: str, file_pattern: str = "*.pdb") -> str:
    """Batch TCR-pMHC complex structure analysis"""
    # 保留原来的验证逻辑
    if not Path(folder_path).exists():
        raise ValueError(f"Folder does not exist: {folder_path}")

    pdb_files = glob.glob(os.path.join(folder_path, file_pattern))
    if not pdb_files:
        raise ValueError(f"No matching files found: {file_pattern}")

    pdb_list = "\n".join([f"  {i + 1}. {os.path.basename(f)}" for i, f in enumerate(pdb_files)])

    # 保留原来的完整提示内容
    return f"""
{SYSTEM_PROMPT}

## Batch Analysis Task

**Target**: {folder_path} ({len(pdb_files)} files)
**Pattern**: {file_pattern}
**Data Collection File**: C:\\Users\\jiangxiaohang\\Desktop\\analysis_data.txt

### File List
{pdb_list}

### Execution Plan
For each file:
1. **Clean workspace**: `delete all` before loading new structure
2. **Load and verify** structure in PyMOL
3. **Complete enhanced analysis** following the workflow above
4. **Write all results** to analysis_data.txt immediately after each calculation
5. **Verify atom counts** after each step
6. **Append results** to CSV file with quality flags
7. **Progress tracking** (X/{len(pdb_files)} completed)

### Batch-Specific Requirements
- Initialize analysis_data.txt at start
- Continue processing if single file fails
- Real-time progress display with biological validation status
- Unified CSV output (append mode)
- Error recovery for problematic structures
- Final summary report with validation statistics
- Read analysis_data.txt at end to verify all data collected

Start enhanced batch processing!
"""


@mcp.prompt()
async def single_analysis(pdb_file_path: str) -> str:
    """Single TCR-pMHC complex structure analysis"""
    # 保留原来的验证逻辑
    if not Path(pdb_file_path).exists():
        raise ValueError(f"PDB file does not exist: {pdb_file_path}")

    pdb_id = Path(pdb_file_path).stem.upper()

    # 保留原来的完整提示内容
    return f"""
{SYSTEM_PROMPT}

## Single File Analysis Task

**Target**: {os.path.basename(pdb_file_path)}
**Path**: {pdb_file_path}
**PDB ID**: {pdb_id}
**Data Collection File**: C:\\Users\\jiangxiaohang\\Desktop\\analysis_data.txt

### Execution Plan
1. **Initialize data file**: Clear/create analysis_data.txt
2. **Clean workspace**: Ensure clean PyMOL environment
3. **Load structure** and verify basic properties
4. **Execute enhanced analysis workflow** as detailed above
5. **Write each result** to analysis_data.txt immediately after calculation
6. **Verify atom counts** after each major step
7. **Read analysis_data.txt** for verification and data compilation
8. **Generate CSV output** (overwrite mode for single file)

### Critical Reminders
- Verify peptide actual sequence before analysis
- Use binding angle complement if > 90°
- Immediate cleanup of all temporary selections
- Write all PyMOL calculation results to analysis_data.txt
- Read analysis_data.txt at end to compile final CSV

### Data Writing Example:
After each calculation, use:
`open('C:/Users/jiangxiaohang/Desktop/analysis_data.txt','a').write(f"Metric: {value}\\n")`

Start enhanced analysis!
"""

    return GetPromptResult(
        description=f"Enhanced single file analysis - {pdb_id} with biological validation",
        messages=[PromptMessage(role="user", content=TextContent(type="text", text=prompt))]
    )

else:
raise ValueError(f"Unknown analysis type: {name}")

if __name__ == "__main__":
    mcp.run()